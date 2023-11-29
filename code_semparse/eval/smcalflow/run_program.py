# noinspection PyUnresolvedReferences
from typing import Optional, List, Dict, Tuple, Union

# noinspection PyUnresolvedReferences
from eval.smcalflow.data.datamodel import *


def run_program(code):
    try:
        if "import" in code:
            raise ValueError("Import is not allowed")
        if "open(" in code:
            raise ValueError("Open is not allowed")
        if "eval(" in code:
            raise ValueError("Eval is not allowed")
        if "exec(" in code:
            raise ValueError("Exec is not allowed")
        if "compile(" in code:
            raise ValueError("Compile is not allowed")

        globals()["api"].last_created_event = None
        exec(code)
        locals()["answer"]()
        dataflow_exp = globals()["api"].last_created_event
        return {
            "success": True,
            "answer": repr_ast(dataflow_exp),
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "answer": None,
            "error": str(e),
        }
