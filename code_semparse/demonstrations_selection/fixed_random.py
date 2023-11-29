from random import Random
from typing import List, Dict

from demonstrations_selection.demonstrations_selector import DemonstrationsSelector


class FixedRandomDemonstrationsSelector(DemonstrationsSelector):
    def pick_demonstrations(self, gold_ex: Dict) -> List[Dict]:
        # we want to have the same random seed every time we pick the demonstrations
        rand = Random(self._seed)

        if "dataflow" in gold_ex and self._n_demonstrations >= 5:
            simple_org_examples = [ex for ex in self._train_examples if "simple_orgchart" in ex["tags"]]

            # include 2 examples from simple_org_examples and the rest from the rest of the examples
            n_simple_org_examples = min(len(simple_org_examples), 2)
            n_rest_examples = min(len(self._train_examples) - len(simple_org_examples), self._n_demonstrations - n_simple_org_examples)
            random_sample = rand.sample(simple_org_examples, n_simple_org_examples) + rand.sample([ex for ex in self._train_examples if "simple_orgchart" not in ex["tags"]], n_rest_examples)

            rand.shuffle(random_sample)

            return random_sample

        return rand.sample(self._train_examples, self._n_demonstrations)
