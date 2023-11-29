import hashlib
import sys
import json
import os
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    after_log
)  # for exponential backoff
import openai
import numpy as np
import logging
import dotenv
from tqdm import tqdm


dotenv.load_dotenv()

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


def cache(list_key):
    """Cache the output of a function call in a file under ".cache" directory. The file name is a hash of the input arguments. The context is a json dictionary with input and output"""

    def _hash(*args, **kwargs):
        """Hash the input arguments"""
        return hashlib.md5(str(args).encode() + str(kwargs).encode()).hexdigest()

    def _cache_file(*args, **kwargs):
        """Return the path to the cache file"""
        return os.path.join("~/.cache/llm", _hash(*args, **kwargs) + ".json")

    def _cache(*args, **kwargs):
        """Return the cached output if it exists, otherwise return None"""
        cache_file = _cache_file(*args, **kwargs)
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                return json.load(f)["output"]
        else:
            return None

    def _save_cache(*args, **kwargs):
        """Save the output to the cache file"""
        output = kwargs.pop("output")
        cache_file = _cache_file(*args, **kwargs)
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, "w") as f:
            # dump input/output (make sure input doesn't include output)
            dump = {"output": output, "input": {"args": args, "kwargs": kwargs}}
            json.dump(dump, f)

    def _decorator(func):
        """The decorator"""

        def _wrapper(*args, **kwargs):
            """The wrapper"""
            # Check if the output is cached
            list_of_values = kwargs[list_key]
            kwargs.pop(list_key)

            output, uncached_keys = [None] * len(list_of_values), []
            for i, list_item in enumerate(list_of_values):
                cached_for_item = _cache(*args, **kwargs, **{f"{list_key}_item": list_item})
                if cached_for_item is not None:
                    output[i] = cached_for_item
                else:
                    uncached_keys.append((i, list_item))

            if len(uncached_keys) == 0:
                return output

            # Call the function
            output_for_uncached = func(*args, **kwargs, **{list_key: [k for (p, k) in uncached_keys]})

            # Save the output to the cache
            for (position, list_item), output_item in zip(uncached_keys, output_for_uncached):
                _save_cache(*args, **kwargs, **{f"{list_key}_item": list_item}, output=output_item)
                output[position] = output_item

            return output

        return _wrapper

    return _decorator


@retry(wait=wait_random_exponential(min=10, max=120), stop=stop_after_attempt(15),
       after=after_log(logger, logging.WARNING))
def completion_with_backoff_chat(**kwargs):
    return openai.ChatCompletion.create(**kwargs)


@retry(wait=wait_random_exponential(min=10, max=120), stop=stop_after_attempt(15),
       after=after_log(logger, logging.WARNING))
def completion_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


@cache(list_key="prompts")
def complete_prompts(prompts, model_name, stop=None):
    output = []

    if "gpt" not in model_name and "davinci" not in model_name:
        openai.api_base = "(vllm-url)"

    if "gpt-3.5" in model_name or model_name == "gpt-4":
        # doesn't support batching...
        assert len(prompts) == 1

        completion_func = completion_with_backoff_chat

        completions = completion_func(
            model=model_name,
            messages=[{"role": "user", "content": prompts[0]}],
            max_tokens=500,
            stop=stop,
            temperature=0,
            request_timeout=60,
        )

        return [{"text": completions["choices"][0]["message"]["content"]}]
    elif "davinci" in model_name:
        completion_func = completion_with_backoff

        completions = completion_func(
            model=model_name,
            prompt=prompts,
            max_tokens=500,
            stop=stop,
            temperature=0,
            logprobs=1,
            request_timeout=60,
        )

        for completion in completions['choices']:
            text = completion['text'].strip()
            token_logprobs = completion['logprobs']['token_logprobs']
            avg_logprob = float(np.mean(token_logprobs))
            output.append({
                "text": text,
                "avg_logprob": avg_logprob,
            })

        return output
    else:
        # no batch, completion api
        assert len(prompts) == 1
        completion_func = completion_with_backoff

        completions = completion_func(
            model=model_name,
            prompt=prompts,
            max_tokens=250,
            stop=stop,
            temperature=0,
            logprobs=1,
            request_timeout=60,
        )

        for completion in completions['choices']:
            text = completion['text'].strip()
            token_logprobs = completion['logprobs']['token_logprobs']
            avg_logprob = float(np.mean(token_logprobs))
            output.append({
                "text": text,
                "avg_logprob": avg_logprob,
            })

        return output


def complete_all(prompts, model_name, stop=None, batch_size=10):
    all_predictions = []

    if True or "gpt-3.5-turbo" in model_name or model_name == "gpt-4":
        # doesn't support batching...
        for prompt in tqdm(prompts, desc=f"Generating {model_name} predictions"):
            predictions = complete_prompts(prompts=[prompt], model_name=model_name, stop=stop)
            all_predictions += [p["text"].strip("` \n").rstrip() for p in predictions]
    else:
        prompt_batches = [prompts[i:i + batch_size] for i in range(0, len(prompts), batch_size)]
        for batch in tqdm(prompt_batches, desc=f"Generating {model_name} predictions"):
            predictions = complete_prompts(prompts=batch, model_name=model_name, stop=stop)
            all_predictions += [p["text"].strip("` \n").rstrip() for p in predictions]

    return all_predictions
