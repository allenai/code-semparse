import re

from eval.overnight.data.datamodel import Person, API
from eval.overnight.dcs import execute_dcs, reverse_simplify_expr
from eval.overnight.run_program import run_program


def parse_gold_answer(gold_answer):
    answer = set([a for a in re.findall(r"\(\w* ([^ ^\)^\(]*)", gold_answer) if a and a != "name"])
    return set([a.split(".")[-1] for a in answer])

def value_to_string(value):
    if type(value) is list or type(value) is set:
        return [value_to_string(v) for v in value]
    elif type(value) is Person:
        return value.name.split(".")[-1]
    elif "." in str(value):
        return str(value).split(".")[-1]
    elif type(value) is int:
        return str(value)


def evaluate_overnight_python(prediction, ex, prompt_method):
    exec_result = run_program(prediction)
    gold_answer = execute_dcs(ex["dcs"], ex["domain"])

    parsed_pred_answer = set()
    if exec_result["answer"]:
        parsed_pred_answer = value_to_string(exec_result["answer"])
        if type(parsed_pred_answer) is list:
            if any(type(item) is not str for item in parsed_pred_answer):
                parsed_pred_answer = None
            else:
                parsed_pred_answer = set(parsed_pred_answer)
    parsed_gold_answer = parse_gold_answer(gold_answer)

    if type(parsed_pred_answer) is set and len(parsed_pred_answer) == 1:
        parsed_pred_answer = list(parsed_pred_answer)[0]
    if type(parsed_gold_answer) is set and len(parsed_gold_answer) == 1:
        parsed_gold_answer = list(parsed_gold_answer)[0]

    denotation_accuracy = parsed_pred_answer == parsed_gold_answer

    return {
        "accuracy": int(denotation_accuracy),
        "denotation_accuracy": int(denotation_accuracy),
        "gold_denotation": list(parsed_gold_answer) if type(parsed_gold_answer) is set else parsed_gold_answer,
        "predicted_denotation": list(parsed_pred_answer) if parsed_pred_answer and type(parsed_pred_answer) is set else parsed_pred_answer,
        "error": exec_result["error"],
    }
