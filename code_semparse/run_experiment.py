import argparse
import os
from random import Random
from typing import Dict, List

import numpy as np
import pandas as pd
from tqdm import tqdm

from demonstrations_selection.bm25_utt import BM25UtteranceDemonstrationsSelector
from demonstrations_selection.oracle_coverage import OracleCoverageDemonstrationsSelector
from eval.evaluate import evaluate
from utils.dataset_reader_utils import get_dataset
from utils.llm_utils import complete_all
from utils.prompt_gen_utils import create_prompt
from demonstrations_selection.fixed_coverage import FixedCoverageDemonstrationsSelector
from demonstrations_selection.fixed_random import FixedRandomDemonstrationsSelector
from demonstrations_selection.demonstrations_selector import DemonstrationsSelector


def get_args():
    args = argparse.ArgumentParser()
    args.add_argument("--dataset_name", type=str, default="geo880")
    args.add_argument("--overnight_domain", type=str)
    args.add_argument("--split_name", type=str, default="tmcd_1")
    args.add_argument("--eval_set_name", type=str, default="test")
    args.add_argument("--n_training_demonstrations", type=int, default=3)
    args.add_argument("--n_test_samples", type=int, default=60)
    args.add_argument("--model", type=str, default="gpt-3.5-turbo")
    args.add_argument("--prompt_lang", type=str)
    args.add_argument("--prompt_method", type=str)
    args.add_argument("--icl_selection_method", type=str, choices=["fixed_random", "cover_atoms_oracle"], default="fixed_random")
    return args.parse_args()


def evaluate_prompt_on_set(demonstrations_selector: DemonstrationsSelector, test_examples: List[Dict], model: str, datatset_name: str,
                           prompt_lang: str, prompt_method: str, program_variation: str = None) -> List[Dict]:
    demonstrations = []
    prompts_for_examples = []
    for ex in tqdm(test_examples):
        ex_demonstrations = demonstrations_selector.pick_demonstrations(ex)
        demonstrations.append(ex_demonstrations)
        prompts_for_examples.append(create_prompt(ex, prompt_lang, prompt_method, ex_demonstrations, datatset_name, program_variation))
    model_predictions = complete_all(prompts_for_examples, model, stop="```")

    results = []
    loop = tqdm(zip(test_examples, prompts_for_examples, model_predictions),
                total=len(test_examples), desc="Evaluating")
    for ex, prompt, prediction in loop:
        result = {
            "qid": ex["qid"],
            "query": ex["query"],
        }

        metrics = evaluate(prediction, ex, datatset_name, prompt_lang)

        result[f"prediction"] = prediction
        result[f"prompt"] = prompt
        for metric_name, metric_value in metrics.items():
            result[f"{metric_name}"] = metric_value
        results.append(result)
        loop.desc = f"Evaluating (avg. accuracy: {np.mean([r['accuracy'] for r in results]):.2f})"

    return results


def get_demonstrations_selector(icl_selection_method: str, examples: List[Dict], n_demonstrations: int, prompt_lang: str, seed: int = 42) -> DemonstrationsSelector:
    if icl_selection_method == "fixed_random":
        return FixedRandomDemonstrationsSelector(examples, n_demonstrations, prompt_lang, seed=seed)
    elif icl_selection_method == "fixed_coverage":
        return FixedCoverageDemonstrationsSelector(examples, n_demonstrations, prompt_lang, seed=seed)
    elif icl_selection_method == "oracle_coverage":
        return OracleCoverageDemonstrationsSelector(examples, n_demonstrations, prompt_lang, seed=seed)
    elif icl_selection_method == "bm25_utt":
        return BM25UtteranceDemonstrationsSelector(examples, n_demonstrations, prompt_lang, seed=seed)
    else:
        raise ValueError(f"ICL selection method {icl_selection_method} is not supported")


def run_experiment(dataset_name: str, split_name: str, n_training_demonstrations: int, n_test_samples: int, model: str,
                   prompt_lang: str, prompt_method: str, program_variation: str = None,
                   icl_selection_method: str = "fixed_random", eval_set: str = None,
                   seed: int = 42, test_seed: int = 42, overnight_domain: str = None, allow_cache=True) -> pd.DataFrame:
    exp_parameters = [model, dataset_name, split_name, n_training_demonstrations, n_test_samples, prompt_lang, prompt_method, program_variation, icl_selection_method, seed]
    if eval_set is not None:
        exp_parameters.append(eval_set)
    output_path = f"../output/results_{'_'.join([str(p) for p in exp_parameters]).replace('/', '-')}.csv"

    if allow_cache and os.path.exists(output_path):
        print(f"Skipping experiment {output_path} because it already exists")
        df = pd.read_csv(output_path)
        return df

    training_set, test_set = get_dataset(dataset_name, split_name, eval_set, overnight_domain)
    demonstrations_selector = get_demonstrations_selector(icl_selection_method, training_set, n_training_demonstrations, prompt_lang, seed=seed)

    sampled_test_set = Random(test_seed).sample(test_set, min(n_test_samples, len(test_set)))

    os.makedirs("../output", exist_ok=True)

    print(
        f"Running {prompt_method} prompt on {n_test_samples} examples from {dataset_name}, {split_name} split")
    results = evaluate_prompt_on_set(demonstrations_selector, sampled_test_set, model, dataset_name, prompt_lang, prompt_method, program_variation)

    # save to csv
    df = pd.DataFrame(results)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(df.select_dtypes(include=np.number).mean())
    print(f"Saving results to {output_path}")
    df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    args = get_args()

    run_experiment(args.dataset_name, args.split_name, args.n_training_demonstrations, args.n_test_samples, args.model,
                   args.prompt_lang, args.prompt_method, None, args.icl_selection_method, args.eval_set_name, overnight_domain=args.overnight_domain)
