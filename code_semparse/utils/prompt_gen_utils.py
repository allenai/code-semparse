from typing import Dict, List

from prompts.prompt_templates import MAIN_TEMPLATE, DEMONSTRATIONS_TEMPLATE, TEMPLATE_PER_DATASET, STRUCTURE_TEMPLATE, \
    PY_TO_PL_DEMONSTRATIONS_TEMPLATE, PL_TO_PY_DEMONSTRATIONS_TEMPLATE, PL_TO_PY_TEMPLATE, PY_TO_PL_TEMPLATE


def create_prompt(ex: Dict, prompt_lang: str, prompt_type: str, demonstrations: List[Dict], dataset_name: str, program_variation: str = None) -> str:
    prompt = MAIN_TEMPLATE

    demonstration_target_type = prompt_lang
    if program_variation:
        demonstration_target_type = f"{prompt_lang}_{program_variation}"

    if prompt_type != "no_dd":
        prompt = prompt.replace("{{structure}}", STRUCTURE_TEMPLATE)
        prompt = prompt.replace("{{structures_for_method}}",
                                TEMPLATE_PER_DATASET[dataset_name]["structure_per_method"][prompt_lang][prompt_type])
    else:
        prompt = prompt.replace("{{structure}}\n", "")

    demonstrations_template = DEMONSTRATIONS_TEMPLATE
    demonstrations_texts = []
    for demonstration in demonstrations:
        demonstration_text = demonstrations_template.replace("{{icl-query}}", demonstration["query"])
        demonstration_text = demonstration_text.replace("{{icl-solution}}", TEMPLATE_PER_DATASET[dataset_name]["solution_prefix_for_method"][prompt_lang] + demonstration[demonstration_target_type])
        demonstrations_texts.append(demonstration_text)
    demonstrations_text = "\n\n".join(demonstrations_texts)

    prompt = prompt.replace("{{demonstrations}}", demonstrations_text)
    prompt = prompt.replace("{{query}}", ex["query"])
    prompt = prompt.replace("{{test_solution_prefix}}",
                            TEMPLATE_PER_DATASET[dataset_name]["test_solution_prefix_for_method"][prompt_lang])

    return prompt


def create_lang_to_py_prompt(ex: Dict, prompt_lang: str, demonstrations: List[Dict], dataset_name: str) -> str:
    return create_lang_conversion_prompt(PL_TO_PY_TEMPLATE, PL_TO_PY_DEMONSTRATIONS_TEMPLATE, ex, prompt_lang, demonstrations, dataset_name)


def create_py_to_lang_prompt(ex: Dict, prompt_lang: str, demonstrations: List[Dict], dataset_name: str) -> str:
    return create_lang_conversion_prompt(PY_TO_PL_TEMPLATE, PY_TO_PL_DEMONSTRATIONS_TEMPLATE, ex, prompt_lang, demonstrations, dataset_name)


def create_lang_conversion_prompt(prompt_template: str, demo_template, ex: Dict, prompt_lang: str, demonstrations: List[Dict], dataset_name: str) -> str:
    prompt = prompt_template

    demonstrations_texts = []
    for demonstration in demonstrations:
        demonstration_text = demo_template
        demonstration_text = demonstration_text.replace("{{pl}}", prompt_lang)
        demonstration_text = demonstration_text.replace("{{icl-query}}", demonstration["query"])
        demonstration_text = demonstration_text.replace("{{icl-python}}", TEMPLATE_PER_DATASET[dataset_name]["solution_prefix_for_method"]["python"] + demonstration["python"])
        demonstration_text = demonstration_text.replace("{{icl-pl}}", demonstration[prompt_lang])
        demonstrations_texts.append(demonstration_text)
    demonstrations_text = "\n\n".join(demonstrations_texts)

    prompt = prompt.replace("{{demonstrations}}", demonstrations_text)
    prompt = prompt.replace("{{python_structure}}",
                            TEMPLATE_PER_DATASET[dataset_name]["structure_per_method"]["python"]["full_dd"])
    prompt = prompt.replace("{{pl_structure}}",
                            TEMPLATE_PER_DATASET[dataset_name]["structure_per_method"][prompt_lang]["full_dd"])
    prompt = prompt.replace("{{pl}}", prompt_lang)

    prompt = prompt.replace("{{query}}", ex["query"])
    if "{{test_python}}" in prompt:
        prompt = prompt.replace("{{test_python}}", ex["python"])
    if "{{test_pl}}" in prompt:
        prompt = prompt.replace("{{test_pl}}", ex[prompt_lang])
    prompt = prompt.replace("{{python_prefix}}",
                            TEMPLATE_PER_DATASET[dataset_name]["solution_prefix_for_method"]["python"])
    prompt = prompt.replace("{{python_test_solution_prefix}}",
                            TEMPLATE_PER_DATASET[dataset_name]["test_solution_prefix_for_method"]["python"])

    return prompt
