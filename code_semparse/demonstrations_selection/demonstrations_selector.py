from abc import ABC, abstractmethod
from random import Random
from typing import List, Dict, Tuple


class DemonstrationsSelector(ABC):
    def __init__(self, train_examples: List[Dict], n_demonstrations, prompt_lang: str, seed: int = 42, should_keep_only_examples_with_python_solution: bool = True):
        self._seed = seed
        self._random = Random(seed)
        self._n_demonstrations = n_demonstrations
        self._prompt_lang = prompt_lang
        self._should_keep_only_examples_with_python_solution = should_keep_only_examples_with_python_solution
        self._train_examples = self._filter_examples(list(train_examples))
        self._random.shuffle(self._train_examples)

        # training_examples = Random(seed).sample([ex for ex in training_examples if "simple_orgchart" in ex["tags"]], 5) + \
        #                     Random(seed).sample([ex for ex in training_examples if "simple_orgchart" not in ex["tags"]], n_training_demonstrations - 5)

    @abstractmethod
    def pick_demonstrations(self, gold: Dict) -> List[Dict]:
        pass

    def _filter_examples(self, all_examples):
        if self._should_keep_only_examples_with_python_solution:
            all_examples = [ex for ex in all_examples if "python" in ex]
        return all_examples
