from transformers import AutoTokenizer
from tqdm import tqdm
import pandas as pd
from dataclasses import dataclass

from lotgi.models.rest import JobExecutionOptionsInput

tqdm.pandas()

TEMPLATE = (
    "We have provided context information below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given this information, please answer the question: {query_str}\n"
)

def estimate_token_usage(input_url : str, prompt : str, model : str, field : str) -> JobExecutionOptionsInput:
    tokenizer = AutoTokenizer.from_pretrained(model)

    inputs = pd.read_json(input_url, lines=True)

    print("Inserting prompt into dataset...")
    inputs[field] = inputs[field].progress_apply(lambda text: TEMPLATE.format(context_str=text, query_str=prompt))

    num_prompt_tokens = len(tokenizer.encode(prompt))
    num_completions = len(inputs)

    def token_count(row) -> int:
        return len(tokenizer.encode(row))

    print("Calculating number of tokens...")
    num_dataset_tokens = inputs[field].progress_map(token_count).sum()

    return JobExecutionOptionsInput(
        model=model,
        input_token_count=(num_prompt_tokens * num_completions) + num_dataset_tokens,
        # TODO: This is an incredibly not-robust estimate.
        num_requests=num_completions,
    )
