import os
import re
import subprocess
import tempfile


def postprocess_lf(lf):
    replacements = [
        ('! ', '!'),
        ('SW', 'edu.stanford.nlp.sempre.overnight.SimpleWorld'),
    ]
    for a, b in replacements:
        lf = lf.replace(a, b)
    return lf


def reverse_simplify_expr(expr):
    # add 'call SW.' before each open parenthesis except for 'lambda' and another '('
    expr = re.sub(r'\((?![\(\s]*lambda|\(|number|var)', r'(call SW.', expr)
    expr = expr.replace("SW.size", ".size")
    # add 'string' to specific tokens
    tokens = ["=", "<", ">", ">=", "<=", "!=", "!type", "gender", "male", "education_start_date", "education_end_date", "employment_start_date", "employment_end_date", "student", "university", "field_of_study", "employee", "employer", "job_title", "logged_in", "birthplace", "friend", "height", "birthdate", "relationship_status", "min", "max", "avg", "sum"]
    for token in tokens:
        expr = re.sub(r'(?<=\s|\()' + re.escape(token) + r'(?=\s|\))', r'(string ' + token + ')', expr)
    # add 'date' to dates
    expr = re.sub(r'\b(\d\d\d\d)\b', r'(date \1 -1 -1)', expr)
    # add 'singleton' to 'en.*' but not 'en.*.*'
    expr = re.sub(r'(call SW.getProperty )(\ben\.\w+\b(?!\.\w+))', r'\1(call SW.singleton \2)', expr)
    return expr

def execute_dcs(query: str, subdomain: str, debug: bool = False):
    reverse_simplify = "call" not in query
    if reverse_simplify:
        query = reverse_simplify_expr(query)
    query = postprocess_lf(query)

    # create a temporary file with the query
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(query)
        f.close()
        query_file = f.name

    prolog_args = ['evaluator/overnight', subdomain, query_file]
    prolog = subprocess.Popen(prolog_args, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.path.dirname(__file__))

    output = prolog.communicate(input=query.encode())[0].decode()

    if "BADJAVA" in output:
        raise Exception("\n".join([l for l in output.split('\n') if "BADJAVA" in l]))

    denotation = [line.split('\t')[1] for line in output.split('\n') if line.startswith('targetValue\t')][0]

    return denotation


def evaluate_overnight_dcs(prediction, ex, prompt_method):
    try:
        predicted_answer = execute_dcs(prediction, subdomain=ex["domain"])
        gold_answer = execute_dcs(ex["dcs"], subdomain=ex["domain"])
        denotation_accuracy = predicted_answer == gold_answer
        error = ""
    except Exception as e:
        error = e
        denotation_accuracy = False
        gold_answer = None
        predicted_answer = None

    exact_match = prediction == ex["dcs"]

    if prediction == ex["dcs"] and not denotation_accuracy:
        execute_dcs(prediction, subdomain=ex["domain"])
        raise Exception("Predicted the same as the gold but got it wrong")

    return {
        "accuracy": int(denotation_accuracy),
        "denotation_accuracy": int(denotation_accuracy),
        "exact_match": int(exact_match),
        "gold_denotation": gold_answer,
        "predicted_denotation": predicted_answer,
        "error": error,
    }

if __name__ == '__main__':
    res = execute_dcs(
        "( call edu.stanford.nlp.sempre.overnight.SimpleWorld.listValue ( call edu.stanford.nlp.sempre.overnight.SimpleWorld.filter ( call edu.stanford.nlp.sempre.overnight.SimpleWorld.getProperty ( call edu.stanford.nlp.sempre.overnight.SimpleWorld.singleton en.block ) ( string !type ) ) ( call edu.stanford.nlp.sempre.overnight.SimpleWorld.ensureNumericProperty ( string length ) ) ( string <= ) ( call edu.stanford.nlp.sempre.overnight.SimpleWorld.ensureNumericEntity ( call edu.stanford.nlp.sempre.overnight.SimpleWorld.getProperty en.block.block1 ( string height ) ) ) ) )",
        "blocks", True)
    print(res)