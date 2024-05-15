from __future__ import annotations

import math
import random
import types
from dataclasses import dataclass
from logging import getLogger
from typing import Any
from typing import Iterator
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple

import numpy.random
import pyarrow
import pyarrow.compute as pc
import torch
import torch.nn.functional as F
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import BatchEncoding
from transformers import PretrainedConfig
from transformers import tokenization_utils_base

from tecton_core.embeddings import execution_utils


logger = getLogger(__name__)

_MAX_INFERENCE_ATTEMPTS = 2
# Fraction of GPU memory to use for the token budget estimation.
_MAX_GPU_ALLOCATION = 0.3
_DEFAULT_GPU_TOKEN_BUDGET = 10_000
_DEFAULT_CPU_TOKEN_BUDGET = 1_000
_MAX_TOKENIZATION_LENGTH = 512
_DEFAULT_TORCH_DTYPE = torch.float32


@dataclass
class InferenceParameters:
    max_input_size: int
    output_size: int
    torch_dtype: torch.dtype
    model_type: str
    _config: PretrainedConfig

    @classmethod
    def from_config(cls, config: PretrainedConfig) -> InferenceParameters:
        return InferenceParameters(
            max_input_size=config.max_position_embeddings or _MAX_TOKENIZATION_LENGTH,
            torch_dtype=config.torch_dtype or _DEFAULT_TORCH_DTYPE,
            output_size=config.hidden_size,
            model_type=config.model_type,
            _config=config,
        )


@dataclass
class ModelContainer:
    tokenizer: tokenization_utils_base.PreTrainedTokenizerBase
    model: torch.nn.Module
    config: InferenceParameters

    @classmethod
    def load(cls, filepath: str, device_name: str) -> ModelContainer:
        with torch.device(device_name):
            model = AutoModel.from_pretrained(
                filepath,
                use_safetensors=True,
                use_cache=False,
                local_files_only=True,
                trust_remote_code=False,
            )
            return cls(
                tokenizer=AutoTokenizer.from_pretrained(filepath, trust_remote_code=False),
                model=model.eval(),
                config=InferenceParameters.from_config(model.config),
            )


# Follows pattern from: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
def _mean_pooling(*, token_embeddings: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    input_mask_expanded = attention_mask.unsqueeze(dim=-1).expand(token_embeddings.size()).to(token_embeddings.dtype)
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, dim=1)
    sum_mask = torch.sum(input_mask_expanded, dim=1)
    # NOTE: clamps to 1e-9 to avoid NaN from the division
    return sum_embeddings / torch.clamp(sum_mask, min=1e-9)


def _embed_pytorch_core_logic(
    *,
    strings: List[str],
    tokenizer: tokenization_utils_base.PreTrainedTokenizerBase,
    model: torch.nn.Module,
    config: InferenceParameters,
) -> torch.Tensor:
    # NOTE: we do the tokenization inline becauase our interchange format is arrow, and this allows
    # us to construct tensors directly on the appropriate device.
    # This is an expedient decision and has not yet been validated as the "right" approach.
    # TODO: Remove max_length once we have a better understanding of how to acquire tokenization limits
    encoded_input = tokenizer(
        strings, padding=True, truncation=True, return_tensors="pt", max_length=config.max_input_size
    )
    with torch.no_grad():
        model_output = model(**encoded_input)

    # TODO: encapsulate this as its own nn.Module so we can have a single nn.Module representation of our model.
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    sentence_embeddings = _mean_pooling(
        token_embeddings=token_embeddings, attention_mask=encoded_input["attention_mask"]
    )
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
    return sentence_embeddings


def _embed_pytorch_core_logic_with_bisect(
    *,
    strings: List[str],
    tokenizer: tokenization_utils_base.PreTrainedTokenizerBase,
    model: torch.nn.Module,
    config: InferenceParameters,
) -> torch.Tensor:
    mid_point = len(strings) // 2
    first_chunk, second_chunk = strings[:mid_point], strings[mid_point:]
    return torch.cat(
        [
            _embed_pytorch_core_logic(strings=first_chunk, tokenizer=tokenizer, model=model, config=config),
            _embed_pytorch_core_logic(strings=second_chunk, tokenizer=tokenizer, model=model, config=config),
        ]
    )


def _embed_pytorch_core_logic_with_retries(
    *,
    strings: List[str],
    tokenizer: tokenization_utils_base.PreTrainedTokenizerBase,
    model: torch.nn.Module,
    config: InferenceParameters,
    max_attempts: int = _MAX_INFERENCE_ATTEMPTS,
) -> torch.Tensor:
    while max_attempts > 0:
        max_attempts -= 1
        try:
            return _embed_pytorch_core_logic(strings=strings, tokenizer=tokenizer, model=model, config=config)
        except torch.cuda.OutOfMemoryError as oom_exc:
            logger.warning(torch.cuda.memory_summary())
            logger.warning(f"Out of Memory. {oom_exc}\n Trying again {max_attempts} more time(s).")
            execution_utils.gc_all(torch.cuda.current_device())
            if max_attempts == 0:
                break
    logger.warning("Failed to embed strings after multiple attempts. Bisecting batch and trying again.")
    return _embed_pytorch_core_logic_with_bisect(strings=strings, tokenizer=tokenizer, model=model, config=config)


def _convert_pytorch_to_arrow(sentence_embeddings: torch.Tensor, num_nulls_end: int = 0) -> pyarrow.Array:
    if len(sentence_embeddings.shape) != 2:
        msg = f"Cannot convert torch.Tensor of shape: {sentence_embeddings.shape}, must be a 2d tensor."
        raise ValueError(msg)
    if sentence_embeddings.dtype != torch.float32:
        msg = f"Cannot convert torch.Tensor of dtype: {sentence_embeddings.dtype}, must be torch.float32."
        raise ValueError(msg)

    sentence_embeddings = sentence_embeddings.cpu().numpy()

    # NOTE: we need to convert our sentence_embeddings to a list and pad it with any nulls.
    sentence_embeddings = [*sentence_embeddings, *(None for _ in range(num_nulls_end))]

    # NOTE: using dynamic sized pyarrow list due to https://github.com/apache/arrow/issues/35697
    return pyarrow.array(list(sentence_embeddings), type=pyarrow.list_(pyarrow.float32()))


def _random_string(tokenizer: tokenization_utils_base.PreTrainedTokenizerBase, max_tokens_in_string: int) -> str:
    num_tokens = numpy.random.randint(3, max_tokens_in_string)
    random_token_ids = numpy.random.randint(0, tokenizer.vocab_size, size=num_tokens)
    tokens = tokenizer.convert_ids_to_tokens(random_token_ids)
    return tokenizer.convert_tokens_to_string(tokens)


def _record_batch_from_vocab(
    tokenizer: tokenization_utils_base.PreTrainedTokenizerBase, tokens_per_line: int, rows: int, column_name: str
) -> pyarrow.RecordBatch:
    text_array = []
    vocab = list(tokenizer.get_vocab().keys())
    # TODO replace below with _random_string once we use tokenization before batching
    for i in range(rows):
        text_array.append(
            {column_name: " ".join([random.choice(vocab) for _ in range(random.randint(3, tokens_per_line))])}
        )
    schema = pyarrow.schema([pyarrow.field(column_name, pyarrow.string())])
    return pyarrow.RecordBatch.from_pylist(text_array, schema=schema)


def _embed_pytorch(
    *,
    batch: pyarrow.RecordBatch,
    tokenizer: tokenization_utils_base.PreTrainedTokenizerBase,
    model: torch.nn.Module,
    config: InferenceParameters,
    input_column_name: str,
    output_column_name: str,
) -> pyarrow.RecordBatch:
    input_column = batch.column(input_column_name)
    null_index = pc.index(pc.is_null(input_column), pyarrow.scalar(True)).as_py()
    if null_index == 0:
        # NOTE: this case means that they are all null! Short circuit and create the embeddings directly.
        sentence_embeddings = pyarrow.nulls(len(input_column), pyarrow.list_(pyarrow.float32()))
    else:
        if null_index > -1:
            rest_null = pc.all(pc.is_null(input_column.slice(null_index))).as_py()
            if not rest_null:
                msg = "Unexpected non-null values after null, maybe not sorting correctly"
                raise ValueError(msg)
            input_strings = input_column.slice(length=null_index).to_pylist()
        else:
            input_strings = input_column.to_pylist()

        sentence_embeddings = _embed_pytorch_core_logic_with_retries(
            strings=input_strings, tokenizer=tokenizer, model=model, config=config
        )

        num_nulls = len(input_column) - null_index if null_index > -1 else 0
        sentence_embeddings = _convert_pytorch_to_arrow(sentence_embeddings, num_nulls_end=num_nulls)

    batch_with_results = pyarrow.RecordBatch.from_arrays(
        [*batch.columns, sentence_embeddings],
        schema=batch.schema.append(pyarrow.field(output_column_name, sentence_embeddings.type)),
    )
    return batch_with_results


def _token_budget_from_tokens(tokens: BatchEncoding) -> int:
    total_tokens = 0
    for i in range(len(tokens.items())):
        total_tokens += len(tokens.tokens(i))
    return total_tokens


def embed_pytorch(
    batch: pyarrow.RecordBatch,
    *,
    model: ModelContainer,
    input_column_name: str,
    output_column_name: str,
    cuda_device: str,
) -> pyarrow.RecordBatch:
    with torch.device(cuda_device):
        results = _embed_pytorch(
            batch=batch,
            tokenizer=model.tokenizer,
            model=model.model,
            config=model.config,
            input_column_name=input_column_name,
            output_column_name=output_column_name,
        )
    return results


def _estimate_token_budget_for_gpu(
    inference_info: Tuple[execution_utils.ModelCallable, Sequence[execution_utils.FuncConfig]],
) -> int:
    """
    Estimate the token budget for a given model on a GPU by running inference on a small batch of data that is
    generated from the token vocabulary in the model's vocabulary. The amount of memory used on the GPU for that small
    batch is then used to infer the amount of memory that would be used by a larger batch and worked back into a
    token budget.

    This method is not perfect and has some limitations:
    * The method to estimate the number of tokens from a string's length get more inaccurate as the strings gets shorter,
    due small strings having a less consistent number of tokens per character.
    * A small increase in the number of tokens can dramatically increase the size of the array due to padding, thereby
      increasing the memory usage.
    * GPU_MEMORY_FRACTION is set to a lower number since the number of tokens per line is determined by the line that
      expands to the most tokens.
    """
    inference_func, inference_config = inference_info
    inference_kwargs = inference_config[0].load().kwargs()
    model_container: ModelContainer = inference_kwargs["model"]
    input_column_name = inference_kwargs["input_column_name"]
    batches_to_estimate = 3
    synthetic_batch = _record_batch_from_vocab(model_container.tokenizer, 300, 10000, input_column_name)
    batches = list(
        dynamic_token_batching(synthetic_batch, token_budget=_DEFAULT_GPU_TOKEN_BUDGET, column_name=input_column_name)
    )
    print("Estimating token budget for GPU.")
    with torch.device("cuda:0"):
        budgets = []
        for dynamic_batch in batches[:batches_to_estimate]:
            memory_tracker = execution_utils.CudaMemoryTracker("cuda:0")
            with memory_tracker:
                _embed_pytorch(
                    batch=dynamic_batch,
                    tokenizer=inference_kwargs["model"].tokenizer,
                    model=inference_kwargs["model"].model,
                    config=inference_kwargs["model"].config,
                    input_column_name=inference_kwargs["input_column_name"],
                    output_column_name=inference_kwargs["output_column_name"],
                )
            # See doc string for explanation of the formula
            memory_usage = memory_tracker.get_usage_data()
            max_token_budget = memory_usage.max_token_budget_from_mem_alloc(_DEFAULT_GPU_TOKEN_BUDGET)
            estimated_safe_token_budget = int(max_token_budget * _MAX_GPU_ALLOCATION)
            budgets.append(estimated_safe_token_budget)
        print(f"Estimated token budgets: {budgets}, using {min(budgets)} as the budget.")
        return min(budgets)


def estimate_token_budget(
    inference: Tuple[execution_utils.ModelCallable, Sequence[execution_utils.FuncConfig]],
    device_type: str,
) -> int:
    if device_type == "cpu":
        print(
            f"No estimation method implemented for CPU, using default CPU token budget of {_DEFAULT_CPU_TOKEN_BUDGET}."
        )
        return _DEFAULT_CPU_TOKEN_BUDGET
    else:
        try:
            token_budget = _estimate_token_budget_for_gpu(inference)
            if token_budget <= 0:
                msg = "Token budget estimation returned a negative value."
                raise ValueError(msg)
            return token_budget
        except Exception as e:
            logger.warning(f"Failed to estimate token budget for GPU: {e}")
            return _DEFAULT_GPU_TOKEN_BUDGET


class ImmutableFuncConfig:
    def __init__(self, **kwargs):
        self._data = types.MappingProxyType(dict(**kwargs))

    def load(self):
        return self

    def kwargs(self) -> Mapping[str, Any]:
        return self._data


@dataclass
class EmbedPytorchFuncConfig:
    _model_filename: str
    _cuda_device: str
    _extra_kwargs: Mapping[str, Any]

    # NOTE: these are late init objects
    _final_kwargs: Optional[Mapping[str, Any]] = None

    @classmethod
    def create(
        cls, model_filename: str, cuda_device: str, input_column_name: str, output_column_name: str
    ) -> EmbedPytorchFuncConfig:
        return cls(
            _model_filename=model_filename,
            _cuda_device=cuda_device,
            _extra_kwargs=types.MappingProxyType(
                {
                    "cuda_device": cuda_device,
                    "input_column_name": input_column_name,
                    "output_column_name": output_column_name,
                }
            ),
        )

    def load(self):
        model_container = ModelContainer.load(self._model_filename, device_name=self._cuda_device)
        self._final_kwargs = types.MappingProxyType(dict(model=model_container, **self._extra_kwargs))
        return self

    def kwargs(self) -> Mapping[str, Any]:
        if self._final_kwargs is None:
            msg = "`load` must be called prior to calling `kwargs`."
            raise ValueError(msg)
        return self._final_kwargs


def dynamic_token_batching(
    batch: pyarrow.RecordBatch, *, token_budget: int, column_name: str
) -> Iterator[pyarrow.RecordBatch]:
    """Split the batch into a set of microbatches.

    The logic for the split is as follows:
    1. token_budget is specified
    2. the data should be sorted according to the sentence length of the "column_name" column.
    3. we calculate how many rows can fit within our token budget w/ padding
    4. the other data in that row should still be maintained
    """
    col = batch.column(column_name)

    lengths = pc.utf8_length(col)
    sorted_indices = pc.array_sort_indices(lengths, order="descending")

    index = 0

    while index < batch.num_rows:
        # Estimated tokens is based on an average token length of 4 chars + 2 tokens for the start/end tokens.
        string_length = lengths[sorted_indices[index].as_py()].as_py()
        if string_length:
            estimated_num_tokens = 2 + math.ceil(string_length / 4)

            #  Calculate the number of rows we can support according to our token budget (assumes padding)
            #  This is simply `budget // estimated_token_count` since our data is sorted by length desc.
            #  NOTE: we ensure that we always take one item in the case that our token budget is smaller than
            #  a single row.
            num_rows = max((token_budget // estimated_num_tokens), 1)
            end = min(index + num_rows, batch.num_rows)
            batch_indices = sorted_indices.slice(index, end - index)
            yield batch.take(batch_indices)
            index = end
        else:
            # NOTE: this case means the rest are all empty. Make the batch the rest of the data!
            # Default slice is unbounded to the end.
            batch_indices = sorted_indices.slice(index)
            yield batch.take(batch_indices)
            index = batch.num_rows


class DynamicBatchingFuncConfig(ImmutableFuncConfig):
    @classmethod
    def create(cls, token_budget: int, column_name: str) -> DynamicBatchingFuncConfig:
        return cls(token_budget=token_budget, column_name=column_name)
