# noinspection PyUnresolvedReferences
from typing import Optional, List, Dict, Tuple, Union

# noinspection PyUnresolvedReferences
from eval.overnight.data.datamodel import *

api = API.from_file("eval/overnight/data/db_socialnetwork.json")


def run_program(code, case_insensitive=True):
    try:
        if "import" in code:
            raise ValueError("Import is not allowed")
        if "open" in code:
            raise ValueError("Open is not allowed")
        if "eval" in code:
            raise ValueError("Eval is not allowed")
        if "exec" in code:
            raise ValueError("Exec is not allowed")
        if "compile" in code:
            raise ValueError("Compile is not allowed")
        exec(code)
        return {
            "success": True,
            "answer": locals()["answer"](),
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "answer": None,
            "error": str(e),
        }
