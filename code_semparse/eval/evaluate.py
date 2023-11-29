# from datasets.top.top_dsl_helper import parse_top_input_to_tree
from typing import Callable

from eval.geo880.funql import evaluate_geo_funql
from eval.geo880.python import evaluate_geo_python
from eval.overnight.dcs import evaluate_overnight_dcs
from eval.overnight.python import evaluate_overnight_python
from eval.pl_to_python import GPTPLToPythonConverter
from eval.smcalflow.simplified import evaluate_smcalflow_simplified
from eval.smcalflow.dataflow import evaluate_smcalflow_dataflow
from eval.smcalflow.python import evaluate_smcalflow_python


def exact_match_eval(prediction, ex, prompt_method):
    gold_target = ex.get(prompt_method)
    return {
        "accuracy": int(prediction.lower() == gold_target.lower()),
        "exact_match": int(prediction.lower() == gold_target.lower()),
        "predicted_target": prediction
    }


def evaluate_pl(eval_fn: Callable):
    def eval_pl(prediction, ex, prompt_lang):
        ex = dict(ex)
        ex[prompt_lang] = prediction
        ex["python"] = GPTPLToPythonConverter.get_instance(ex["dataset"], prompt_lang, ex.get("domain")).convert_pl_to_python(prompt_lang, ex)
        eval_result = eval_fn(ex["python"], ex, "python")

        if not eval_result["accuracy"]:
            ex["python"] = GPTPLToPythonConverter.get_instance(ex["dataset"], prompt_lang, ex.get("domain")).convert_pl_to_python(prompt_lang, ex, model_name="gpt-4")
            eval_result = eval_fn(ex["python"], ex, "python")
        eval_result["converted_python"] = ex["python"]
        return eval_result

    return eval_pl


dataset_and_mr_to_eval_func = {
    "geo880": {
        "python": evaluate_geo_python,
        "scala": evaluate_pl(evaluate_geo_python),
        "javascript": evaluate_pl(evaluate_geo_python),
        "funql": evaluate_geo_funql,
        "prolog": exact_match_eval,
    },
    "smcalflow": {
        "simplified": evaluate_smcalflow_simplified,
        "dataflow": evaluate_smcalflow_dataflow,
        "python": evaluate_smcalflow_python,
        "javascript": evaluate_pl(evaluate_smcalflow_python),
        "scala": evaluate_pl(evaluate_smcalflow_python),
    },
    "overnight": {
        "dcs": evaluate_overnight_dcs,
        "dcs_simplified": evaluate_overnight_dcs,
        "scala": evaluate_pl(evaluate_overnight_python),
        "javascript": evaluate_pl(evaluate_overnight_python),
        "python": evaluate_overnight_python,
    }
}


def evaluate(prediction, ex, datatset_name, prompt_lang):
    if datatset_name not in dataset_and_mr_to_eval_func:
        raise ValueError(f"Eval for dataset {datatset_name} is not supported")
    if prompt_lang not in dataset_and_mr_to_eval_func[datatset_name]:
        raise ValueError(f"Eval for prompt type {prompt_lang} is not supported")

    eval_fn = dataset_and_mr_to_eval_func[datatset_name][prompt_lang]

    return eval_fn(prediction, ex, prompt_lang)
