from prompts.geo880 import python as geo880_python, funql as geo880_funql, scala as geo880_scala, javascript as geo880_javascript
from prompts.smcalflow import simplified as smcalflow_cs_simple_v3_simplified, python as smcalflow_cs_simple_v3_python, dataflow as smcalflow_cs_simple_v3_dataflow, javascript as smcalflow_cs_simple_v3_javascript, scala as smcalflow_cs_simple_v3_scala
from prompts.overnight import python as overnight_python, dcs as overnight_dcs, scala as overnight_scala, javascript as overnight_javascript, dcs_simplified as overnight_dcs_simplified

MAIN_TEMPLATE = """
{{structure}}
Write code to solve the following queries:
{{demonstrations}}

query: {{query}}
solution: ```
{{test_solution_prefix}}""".lstrip()

PY_TO_PL_TEMPLATE = """
Given the following python data structures and functions:
{{python_structure}}

and the corresponding {{pl}} data structures and functions:
{{pl_structure}}

convert the following python functions to {{pl}}:
{{demonstrations}}

query: {{query}}
python: ```python
{{python_prefix}}{{test_python}}
```
{{pl}}: ```{{pl}}
""".strip()

# since this is used for eval, we don't need to include the query
PL_TO_PY_TEMPLATE = """
Given the following python data structures and functions:
{{python_structure}}

and the corresponding {{pl}} data structures and functions:
{{pl_structure}}

convert the following {{pl}} functions to python:
{{demonstrations}}

{{pl}}: ```{{pl}}
{{test_pl}}
```
python: ```python
{{python_test_solution_prefix}}
""".strip()

STRUCTURE_TEMPLATE = """
Given the following data structures and functions:
{{structures_for_method}}
""".lstrip()

TEMPLATE_PER_DATASET = {
    "geo880": {
        "structure_per_method": {
            "python": geo880_python.structures,
            "scala": geo880_scala.structures,
            "javascript": geo880_javascript.structures,
            "funql": geo880_funql.structures
        },
        "solution_prefix_for_method": {
            "python": geo880_python.solution_prefix,
            "scala": geo880_scala.solution_prefix,
            "javascript": geo880_javascript.solution_prefix,
            "funql": geo880_funql.solution_prefix
        },
        "test_solution_prefix_for_method": {
            "python": geo880_python.test_solution_prefix,
            "scala": geo880_scala.test_solution_prefix,
            "javascript": geo880_javascript.test_solution_prefix,
            "funql": geo880_funql.test_solution_prefix
        }
    },
    "smcalflow": {
        "structure_per_method": {
            "simplified": smcalflow_cs_simple_v3_simplified.structures,
            "dataflow": smcalflow_cs_simple_v3_dataflow.structures,
            "python": smcalflow_cs_simple_v3_python.structures,
            "javascript": smcalflow_cs_simple_v3_javascript.structures,
            "scala": smcalflow_cs_simple_v3_scala.structures
        },
        "solution_prefix_for_method": {
            "simplified": smcalflow_cs_simple_v3_simplified.solution_prefix,
            "dataflow": smcalflow_cs_simple_v3_dataflow.solution_prefix,
            "python": smcalflow_cs_simple_v3_python.solution_prefix,
            "javascript": smcalflow_cs_simple_v3_javascript.solution_prefix,
            "scala": smcalflow_cs_simple_v3_scala.solution_prefix
        },
        "test_solution_prefix_for_method": {
            "simplified": smcalflow_cs_simple_v3_simplified.test_solution_prefix,
            "dataflow": smcalflow_cs_simple_v3_dataflow.test_solution_prefix,
            "python": smcalflow_cs_simple_v3_python.test_solution_prefix,
            "javascript": smcalflow_cs_simple_v3_javascript.test_solution_prefix,
            "scala": smcalflow_cs_simple_v3_scala.test_solution_prefix
        }
    },
    "overnight": {
        "structure_per_method": {
            "python": overnight_python.structures,
            "scala": overnight_scala.structures,
            "javascript": overnight_javascript.structures,
            "dcs": overnight_dcs.structures,
            "dcs_simplified": overnight_dcs_simplified.structures,
        },
        "solution_prefix_for_method": {
            "python": overnight_python.solution_prefix,
            "scala": overnight_scala.solution_prefix,
            "javascript": overnight_javascript.solution_prefix,
            "dcs": overnight_dcs.solution_prefix,
            "dcs_simplified": overnight_dcs_simplified.solution_prefix,
        },
        "test_solution_prefix_for_method": {
            "python": overnight_python.test_solution_prefix,
            "scala": overnight_scala.test_solution_prefix,
            "javascript": overnight_javascript.test_solution_prefix,
            "dcs": overnight_dcs.test_solution_prefix,
            "dcs_simplified": overnight_dcs_simplified.test_solution_prefix,
        }
    }
}

DEMONSTRATIONS_TEMPLATE = """
query: {{icl-query}}
solution: ```
{{icl-solution}}
```""".strip()

PY_TO_PL_DEMONSTRATIONS_TEMPLATE = """
query: {{icl-query}}
python: ```python
{{icl-python}}
```
{{pl}}: ```{{pl}}
{{icl-pl}}
```"""

PL_TO_PY_DEMONSTRATIONS_TEMPLATE = """
{{pl}}: ```{{pl}}
{{icl-pl}}
```
python: ```python
{{icl-python}}
```"""
