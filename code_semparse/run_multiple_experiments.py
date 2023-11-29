import argparse
import itertools
import os
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

import pandas as pd


def run_experiment_wrapper(args):
    dataset_name, split, eval_set, n_training_demonstrations, n_test_samples, model, prompt_lang, prompt_method, program_variation, demonstrations_selection_method, seed, overnight_domain, allow_cache, i = args
    print(f"\n *** Running dataset: {dataset_name}, split: {split}, n_training_demonstrations: {n_training_demonstrations}, prompt_lang: {prompt_lang}, prompt_method: {prompt_method}")

    # this is needed for multiprocessing
    os.environ['OPENDF_DB_FILENAME'] = f"test_{i}.db"

    # only after setting the env variable, we can import the run_experiment function (due to the way opendf loads)
    from run_experiment import run_experiment

    results = run_experiment(dataset_name, split, n_training_demonstrations, n_test_samples, model, prompt_lang, prompt_method, program_variation,
                             demonstrations_selection_method, overnight_domain=overnight_domain, seed=seed, test_seed=1, eval_set=eval_set, allow_cache=allow_cache)

    return {
        "dataset_name": dataset_name,
        "split": split,
        "n_training_demonstrations": n_training_demonstrations,
        "prompt_lang": prompt_lang,
        "prompt_method": prompt_method,
        "program_variation": program_variation,
        "demonstrations_selection_method": demonstrations_selection_method,
        "accuracy": results["accuracy"].mean(),
        "exact_match": results["exact_match"].mean() if "exact_match" in results else None,
    }


def run_set_of_experiments(dataset_name, exp_type, model, eval_set=None, n_test_samples=250, seeds=None, allow_cache=True):
    if exp_type in ["curve", "curve_python"]:
        n_training_demonstrations_all = [1, 5, 10, 25]
    else:
        if model == "bigcode/starcoder":
            n_training_demonstrations_all = [5]
        else:
            n_training_demonstrations_all = [10]
    
    if exp_type == "single_multi":
        program_variations = ["oneline", "multiline"]
    else:
        program_variations = [None]

    overnight_domain = None

    if dataset_name == "smcalflow":
        dsl_lang = "dataflow"
        if exp_type == "simplified":
            dsl_lang = "simplified"
        if exp_type in ["curve", "curve_python"]:
            splits_all = ["source_domain_with_target_num0"]
        else:
            splits_all = ["iid", "source_domain_with_target_num0"]
    elif dataset_name == "geo880":
        dsl_lang = "funql"
        if exp_type in ["curve", "curve_python"]:
            splits_all = ["tmcd_1"]
        else:
            splits_all = ["template_1", "tmcd_1", "standard", "length"]
    elif dataset_name == "overnight":
        dsl_lang = "dcs"
        if exp_type == "simplified":
            dsl_lang = "dcs_simplified"
        if exp_type in ["curve", "curve_python"]:
            splits_all = ["template/split_0"]
        else:
            splits_all = ["iid", "template/split_0"]
        overnight_domain = "socialnetwork"
    else:
        raise Exception(f"Unknown dataset: {dataset_name}")

    if exp_type == "coverage":
        demonstrations_selection_methods_per_prompt_lang = {
            "python": ["fixed_coverage"],
            # dsl_lang: ["fixed_coverage"],
        }
        prompt_methods_per_lang = {
            "python": ["full_dd", "no_dd"],
            dsl_lang: ["no_dd"],
        }
    elif exp_type == "single_multi":
        demonstrations_selection_methods_per_prompt_lang = {
            "python": ["fixed_random"],
        }
        prompt_methods_per_lang = {
            "python": ["full_dd"],
        }
    elif exp_type == "pls":
        demonstrations_selection_methods_per_prompt_lang = {
            "python": ["fixed_random"],
            dsl_lang: ["fixed_random"],
            "scala": ["fixed_random"],
            "javascript": ["fixed_random"]
        }
        prompt_methods_per_lang = {
            "python": ["full_dd", "no_dd"],
            dsl_lang: ["full_dd", "no_dd"],
            "scala": ["full_dd", "no_dd"],
            "javascript": ["full_dd", "no_dd"]
        }
    elif exp_type == "curve":
        demonstrations_selection_methods_per_prompt_lang = {
            "python": ["fixed_random"],
            dsl_lang: ["fixed_random"],
        }
        prompt_methods_per_lang = {
            "python": ["full_dd", "no_dd"],
            dsl_lang: ["full_dd", "no_dd"],
        }
    elif exp_type == "curve_python":
        demonstrations_selection_methods_per_prompt_lang = {
            "python": ["fixed_random"],
        }
        prompt_methods_per_lang = {
            "python": ["full_dd", "list_of_operators", "no_typing", "no_dd"],
        }
    elif exp_type == "simplified":
        demonstrations_selection_methods_per_prompt_lang = {
            "python": ["fixed_random"],
            dsl_lang: ["fixed_random"],
        }
        prompt_methods_per_lang = {
            "python": ["full_dd", "no_dd"],
            dsl_lang: ["full_dd", "no_dd"],
        }
    elif exp_type == "formal":
        demonstrations_selection_methods_per_prompt_lang = {
            dsl_lang: ["fixed_random"],
        }
        prompt_methods_per_lang = {
            dsl_lang: ["formal", "full_dd", "list_of_operators", "no_dd"],
        }
    else:
        demonstrations_selection_methods_per_prompt_lang = {
            "python": ["fixed_random"],
            dsl_lang: ["fixed_random"],
        }
        prompt_methods_per_lang = {
            dsl_lang: ["full_dd", "list_of_operators", "no_dd"],
            "python": ["full_dd", "no_typing", "list_of_operators", "no_dd"],
        }

    if not seeds:
        seeds = [1, 2, 3]

    combinations = []
    for prompt_lang, sel_method in demonstrations_selection_methods_per_prompt_lang.items():
        for prompt_method in prompt_methods_per_lang[prompt_lang]:
            combinations.extend(list(itertools.product(seeds, splits_all, n_training_demonstrations_all, [prompt_lang], [prompt_method], sel_method, program_variations)))
            print(seeds, splits_all, n_training_demonstrations_all, [prompt_lang], [prompt_method], sel_method, program_variations)

    if exp_type == "curve" and dataset_name == "smcalflow":
        combinations.extend(list(itertools.product(seeds, ["source_domain_with_target_num0"], [15], ["dataflow"], ["full_dd"], ["fixed_random"], program_variations)))
        print(seeds, ["source_domain_with_target_num0"], [15], ["dataflow"], ["full_dd"], ["fixed_random"], program_variations)

    if dataset_name == "smcalflow":
        combinations = [c for c in combinations if not (c[2] > 20 and c[4] == "full_dd" and c[3] == "dataflow")]
    else:
        combinations = [c for c in combinations if not (c[2] > 30 and c[4] not in ["no_dd", "no_typing"])]

    print(f"Total number of experiments: {len(combinations)}")

    num_processes = args.num_processes

    task_indexes = list(range(1, len(combinations)+1))
    args_list = [(dataset_name, split, eval_set, n_training_demonstrations, n_test_samples, model, prompt_lang, prompt_method, program_variation,
                  demonstrations_selection_method, seed, overnight_domain, allow_cache, i) for
                 (seed, split, n_training_demonstrations, prompt_lang, prompt_method, demonstrations_selection_method, program_variation), i
                 in zip(combinations, task_indexes)]

    if num_processes > 1:
        with ProcessPoolExecutor(num_processes) as executor:
            experiments = list(executor.map(run_experiment_wrapper, args_list))
    else:
        experiments = list(map(run_experiment_wrapper, args_list))

    df = pd.DataFrame(experiments)
    df.loc[df['split'].isnull(), 'split'] = "iid"

    if len(program_variations) > 1:
        df = df.groupby(["dataset_name", "split", "n_training_demonstrations", "prompt_lang", "prompt_method", "demonstrations_selection_method", "program_variation"])[["accuracy", "exact_match"]].mean().reset_index()
    else:
        df = df.groupby(["dataset_name", "split", "n_training_demonstrations", "prompt_lang", "prompt_method", "demonstrations_selection_method"])[["accuracy", "exact_match"]].mean().reset_index()

    print(df.to_string(index=False))

    print(f"Finished running {dataset_name} experiments for {exp_type}")

    os.makedirs("../output/agg", exist_ok=True)
    with open(f"../output/agg/results_{dataset_name}_{exp_type}_{model.replace('/', '_')}_{datetime.now().strftime('%H%M')}.txt", "w") as f:
        f.write(df.to_string(index=False))
        f.write("\n\n")

    df.to_csv(f"../output/agg/results_{dataset_name}_{exp_type}_{model.replace('/', '_')}_{datetime.now().strftime('%H%M')}.csv", index=False)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--num-processes", type=int, default=8)
    args = argparser.parse_args()

    run_set_of_experiments("geo880", "pls", "gpt-3.5-turbo")
    run_set_of_experiments("geo880", "main", "bigcode/starcoder", eval_set="test", n_test_samples=400)
    run_set_of_experiments("geo880", "main", "gpt-3.5-turbo", eval_set="test", seeds=[4], n_test_samples=10)
    run_set_of_experiments("geo880", "curve", "gpt-3.5-turbo", n_test_samples=400)
    run_set_of_experiments("geo880", "curve_python", "gpt-3.5-turbo", n_test_samples=400)
    run_set_of_experiments("geo880", "coverage", "gpt-3.5-turbo", n_test_samples=400)
    run_set_of_experiments("geo880", "single_multi", "gpt-3.5-turbo", n_test_samples=400)
    run_set_of_experiments("geo880", "formal", "gpt-3.5-turbo", n_test_samples=400)

    run_set_of_experiments("overnight", "main", "gpt-3.5-turbo")
    run_set_of_experiments("overnight", "main", "bigcode/starcoder")
    run_set_of_experiments("overnight", "curve", "gpt-3.5-turbo")
    run_set_of_experiments("overnight", "curve_python", "gpt-3.5-turbo")
    run_set_of_experiments("overnight", "single_multi", "gpt-3.5-turbo")
    run_set_of_experiments("overnight", "pls", "gpt-3.5-turbo")
    run_set_of_experiments("overnight", "simplified", "gpt-3.5-turbo")

    run_set_of_experiments("smcalflow", "main", "gpt-3.5-turbo", eval_set="test")
    run_set_of_experiments("smcalflow", "main", "bigcode/starcoder", eval_set="test")
    run_set_of_experiments("smcalflow", "curve", "gpt-3.5-turbo")
    run_set_of_experiments("smcalflow", "curve_python", "gpt-3.5-turbo")
    run_set_of_experiments("smcalflow", "single_multi", "gpt-3.5-turbo")
    run_set_of_experiments("smcalflow", "pls", "gpt-3.5-turbo")
    run_set_of_experiments("smcalflow", "simplified", "gpt-3.5-turbo")