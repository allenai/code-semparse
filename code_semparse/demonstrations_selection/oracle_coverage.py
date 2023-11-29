from typing import List, Dict

from demonstrations_selection.demonstrations_selector import DemonstrationsSelector
from demonstrations_selection.greedy import decomposed_coverage_greedy
from demonstrations_selection.structural import recall_stscores_v3
from utils.lf_utils import get_substructs


class OracleCoverageDemonstrationsSelector(DemonstrationsSelector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._demonstrations = []
        self._cand_structs: list[set] = get_substructs([ex["funql"] for ex in self._train_examples], None, 1, verbose=True)

    def pick_demonstrations(self, gold_ex: Dict) -> List[Dict]:
        query_structs = get_substructs([gold_ex['funql']], None, 1, verbose=True)[0]
        cand_stscores = recall_stscores_v3(query_structs, self._cand_structs)
        shot_idxs, stats = decomposed_coverage_greedy(self._n_demonstrations, cand_stscores, None, 1, cand_stscores)
        shot_scores = cand_stscores[shot_idxs].sum(axis=-1)

        return [self._train_examples[idx] for idx in shot_idxs]
