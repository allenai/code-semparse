from eval.smcalflow.dataflow import evaluate_smcalflow_dataflow
from eval.smcalflow.run_program import run_program


def evaluate_smcalflow_python(prediction, ex, prompt_method):
    # first convert python to dataflow, then evaluate using dataflow evaluator

    exec_result = run_program(prediction)
    if not exec_result["success"]:
        return {
            "success": False,
            "denotation_accuracy": 0,
            "accuracy": 0,
            "exact_match": 0,
            "conversion_error": exec_result["error"],
            "gold_simplified": ex["simplified"],
        }
    eval_results = evaluate_smcalflow_dataflow(exec_result["answer"], ex, prompt_method, simplify=False)
    eval_results["converted_dataflow"] = exec_result["answer"]
    eval_results["gold_simplified"] = ex["simplified"]

    return eval_results
