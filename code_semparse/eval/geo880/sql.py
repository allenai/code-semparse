import subprocess

SQLITE_DBPATH = 'eval/geo880/data/geography-db.added-in-2020.sqlite'

def execute_sqlite_query(query):
    sql_args = ['sqlite3', str(SQLITE_DBPATH), query]
    sql = subprocess.Popen(sql_args, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = sql.communicate()
    return out.decode().strip().split('\n')

def evaluate_sql(prediction, ex, prompt_method):
    gold_answer = execute_sqlite_query(ex["sql"])
    predicted_answer = execute_sqlite_query(prediction)

    if type(gold_answer) != list:
        gold_answer = [gold_answer]
    if type(predicted_answer) != list:
        predicted_answer = [predicted_answer]

    denotation_accuracy = set(gold_answer) == set(predicted_answer)
    exact_match = prediction == ex["sql"]

    return {
        "accuracy": int(denotation_accuracy),
        "denotation_accuracy": int(denotation_accuracy),
        "gold_denotation": gold_answer,
        "predicted_denotation": predicted_answer,
        "exact_match": int(exact_match),
        "error": "",
    }