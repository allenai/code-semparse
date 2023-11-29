from typing import List, Dict

from demonstrations_selection.fixed_random import FixedRandomDemonstrationsSelector
from utils.dataset_reader_utils import get_dataset
from utils.llm_utils import complete_all
from utils.prompt_gen_utils import create_lang_to_py_prompt


class GPTPLToPythonConverter:
    __instance_per_dataset_and_pl = {}

    @staticmethod
    def get_instance(dataset_name: str, pl: str, overnight_domain: str = None) -> "GPTPLToPythonConverter":
        if (dataset_name, pl) not in GPTPLToPythonConverter.__instance_per_dataset_and_pl:
            GPTPLToPythonConverter.__instance_per_dataset_and_pl[(dataset_name, pl, overnight_domain)] = GPTPLToPythonConverter(dataset_name, pl, overnight_domain)
        return GPTPLToPythonConverter.__instance_per_dataset_and_pl[(dataset_name, pl, overnight_domain)]

    def __init__(self, dataset_name: str, pl: str, overnight_domain: str = None):
        all_examples, _ = get_dataset(dataset_name, split_name=None, domain=overnight_domain)
        self.examples = [ex for ex in all_examples if ex.get("python") is not None and ex.get(pl) is not None]

    def convert_pl_to_python(self, pl: str, ex: Dict, n_demonstrations: int = 15, model_name="gpt-3.5-turbo"):
        demonstrations_selector = FixedRandomDemonstrationsSelector(
            train_examples=self.examples,
            seed=0,
            n_demonstrations=min(n_demonstrations, len(self.examples)),
            should_keep_only_examples_with_python_solution=True,
            prompt_lang=pl,
        )
        demonstrations = demonstrations_selector.pick_demonstrations(ex)
        prompt = create_lang_to_py_prompt(ex, pl, demonstrations, ex["dataset"])

        model_prediction = complete_all([prompt], model_name, stop="query:")[0]

        return model_prediction
