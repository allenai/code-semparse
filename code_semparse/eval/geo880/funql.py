import os
import subprocess
from pathlib import Path


wasp_eval_path = Path("../wasp-1.0")


def parse_prolog_ans(ans):
    try:
        import ast
        res = ast.literal_eval(ans)
    except:
        import re
        pat = re.compile(r"\b([^(),'\[\]]+)\b")
        res = [m.group(1) for m in pat.finditer(ans)]
    return res

def parse_funql_ans(ans):
    try:
        import ast
        res = ast.literal_eval(ans)
    except:
        import re
        pat = re.compile(r"\('?([^(),']+)'?(,|\))")
        res = [m.group(1) for m in pat.finditer(ans)]
    return res

def get_funql_subprocess(debug: bool =True):
    if not os.path.exists(wasp_eval_path):
        print(f"Could not find wasp-1.0 at {wasp_eval_path}")
        print("Please download it from: http://www.cs.utexas.edu/%7Eml/wasp/wasp-1.0.tar.gz")
        raise "Could not find wasp-1.0"
    prolog_args = ['swipl']
    prolog = subprocess.Popen(prolog_args, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for path in ['geobase.pl', 'geoquery.pl', 'eval.pl']:
        cmd = f"compile('{wasp_eval_path}/data/geo-funql/eval/{path}').\n"
        if debug: print(cmd)
        prolog.stdin.write(cmd.encode())
    return prolog


def execute_funql(
    query: str, debug: bool = False
):
    prolog = get_funql_subprocess(debug)
    cmd = f"execute_funql_query({query}, X), print(X)."
    if debug: print(cmd)
    try:
        answer = prolog.communicate(input=cmd.encode() + b'\n', timeout=10)
        for a in answer[0].decode().split('\n'):
            if a.strip().startswith('[') and a.strip().endswith(']'):
                answer = a.strip()
                if debug: print(answer)
                return answer
    except subprocess.TimeoutExpired:
        print("Timeout swipl", query)
    # print('No answer found. Full output:\n{answer}')
    return None

def evaluate_geo_funql(prediction, ex, prompt_method):
    gold_answer = ex["funql_ans"]
    predicted_answer = execute_funql(prediction, )
    denotation_accuracy = predicted_answer == gold_answer
    exact_match = prediction == ex["funql"]

    return {
        "accuracy": int(denotation_accuracy),
        "denotation_accuracy": int(denotation_accuracy),
        "gold_denotation": gold_answer,
        "predicted_denotation": predicted_answer,
        "exact_match": int(exact_match),
        "error": "",
    }
