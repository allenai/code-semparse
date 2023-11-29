import re
from collections import defaultdict
from typing import List, Dict

import numpy as np

from demonstrations_selection.demonstrations_selector import DemonstrationsSelector
from demonstrations_selection.greedy import decomposed_coverage_greedy
from utils.lf_utils import get_substructs


class FixedCoverageDemonstrationsSelector(DemonstrationsSelector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._demonstrations = []

        cand_structs: list[set] = get_substructs([ex[self._prompt_lang] for ex in self._train_examples], None, subst_size=1, verbose=True, prompt_lang=self._prompt_lang)
        query_structs = sorted(list(set([s for l in cand_structs for s in l])))

        self._random.shuffle(query_structs)
        cand_stscores = np.array([[1 / len(query_structs) if s in _cand_structs else 0 for s in query_structs] for _cand_structs in cand_structs])
        # greedy algorithm from https://arxiv.org/abs/2305.14907 with c(s, z) = 1[s in z]
        # basically maximizing set-recall
        shot_idxs, stats = decomposed_coverage_greedy(
            self._n_demonstrations, cand_stscores, candidates=self._train_examples)
        self._demonstrations = [self._train_examples[idx] for idx in shot_idxs]

        self._covered = stats['score']
        print(f"Coverage of: {stats['score']:.3f}")

    def pick_demonstrations(self, gold_ex: Dict) -> List[Dict]:
        return self._demonstrations
