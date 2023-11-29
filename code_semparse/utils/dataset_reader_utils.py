import json
import os.path
import re


def fix_simple_smcalflow_dataset(examples):
    def replace_with_attendee(input_str):
        # we want to change any case of FindTeamOf( recipient= with_attendee( Jesse ) ) to FindTeamOf( recipient= Jesse )
        pattern = re.compile(r'recipient=\s*with_attendee\((.*?)\)')
        fixed = re.sub(pattern, r'\1', input_str)
        return fixed

    for ex in examples:
        ex["simplified"] = replace_with_attendee(ex["simplified"])


def simplify_overnight_expr(expr):
    expr = re.sub(r'call\s+(SW\.|\.)|\b(date|singleton|string)\b', '', expr)
    expr = re.sub(r'(\d+)\s+-1\s+-1', r'\1', expr)  # simplify dates
    expr = re.sub(r'\(\s*([^\s\(\)]+)\s*\)', r'\1', expr)  # remove parenthesis around single-token expressions
    expr = re.sub(r'\s+', ' ', expr).strip()  # remove extra whitespaces
    return expr

def simplify_overnight(examples):
    for ex in examples:
        ex["original"] = ex["dcs"]
        ex["dcs_simplified"] = simplify_overnight_expr(ex["dcs"])


def get_dataset(dataset_name: str, split_name: str, eval_set: str = None, domain: str = None):
    if domain is None:
        dataset_path = f"../datasets/{dataset_name}/all.jsonl"
        split_path = f"../datasets/{dataset_name}/splits/{split_name}/split.json"
    else:
        dataset_path = f"../datasets/{dataset_name}/{domain}.all.jsonl"
        split_path = f"../datasets/{dataset_name}/splits/{split_name}/{domain}.json"

    with open(dataset_path, "r") as f:
        all_original_examples = [json.loads(line) for line in f]

    if dataset_name == "smcalflow":
        fix_simple_smcalflow_dataset(all_original_examples)
    elif dataset_name == "overnight":
        simplify_overnight(all_original_examples)

    qid_to_example = {ex["qid"]: ex for ex in all_original_examples}

    for ex in all_original_examples:
        ex["dataset"] = dataset_name

    for pl in ["python", "scala", "javascript"]:
        pl_programs_path = f"../datasets/{dataset_name}/all_{pl}_programs.jsonl"
        if os.path.exists(pl_programs_path):
            with open(pl_programs_path, "r") as f:
                all_pl_programs = [json.loads(line) for line in f]

            for ex in all_pl_programs:
                if ex["qid"] in qid_to_example:
                    qid_to_example[ex["qid"]][pl] = ex[pl]
                    if "python_oneline" in ex:
                        qid_to_example[ex["qid"]]["python_oneline"] = ex["python_oneline"]
                    if "python_multiline" in ex:
                        qid_to_example[ex["qid"]]["python_multiline"] = ex["python_multiline"]

    if split_name is None:
        return all_original_examples, all_original_examples
    else:
        with open(split_path, "r") as f:
            split = json.load(f)
            train_qids = split["train"]
            train_examples = [qid_to_example[qid] for qid in train_qids]

            if eval_set is None:
                if "dev" in split:
                    test_set_name = "dev"
                elif "valid" in split:
                    test_set_name = "valid"
                else:
                    test_set_name = "test"
                    # for now let's not use test, except if there's no choice
                    assert (dataset_name == "geo880" and split_name == "standard") or split_name == "concepts" or dataset_name == "overnight" or (dataset_name == "smcalflow" and split_name == "iid")
            else:
                test_set_name = eval_set

            print(f"Loading {test_set_name} set for {dataset_name}/{split_name}")

            test_qids = split[test_set_name]
            test_examples = [qid_to_example[qid] for qid in test_qids]

        return train_examples, test_examples
