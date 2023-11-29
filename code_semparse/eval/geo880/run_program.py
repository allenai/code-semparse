import re

# noinspection PyUnresolvedReferences
from typing import Optional, List, Dict, Tuple, Union

from eval.geo880.data.database import GeoDB

# noinspection PyUnresolvedReferences
from eval.geo880.data.datamodel import State, City, Country, River, Place, Mountain, Lake, GeoModel, longer, higher, lower, max_ignore_nans, min_ignore_nans

geodb = GeoDB.from_db_file("eval/geo880/data/geobase")
geo_model = GeoModel.from_db(geodb)


def run_program(code, case_insensitive=True):
    if case_insensitive:
        # lowercase all strings enclosed in double quotes or single quotes
        code = re.sub(r'\"(.+?)\"', lambda m: '"' + m.group(1).lower() + '"', code)
        code = re.sub(r'\'(.+?)\'', lambda m: "'" + m.group(1).lower() + "'", code)

    code = code.replace("max(", "max_ignore_nans(")
    code = code.replace("min(", "min_ignore_nans(")

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
