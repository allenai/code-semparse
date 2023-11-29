from typing import List, Dict

import numpy as np

from demonstrations_selection.demonstrations_selector import DemonstrationsSelector
from rank_bm25 import BM25Okapi


class BM25UtteranceDemonstrationsSelector(DemonstrationsSelector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tokenized_corpus = [ex["query"].lower().split() for ex in
                            self._train_examples]  # utterances are already tokenized
        self._bm25 = BM25Okapi(tokenized_corpus)

    def pick_demonstrations(self, gold_ex: Dict) -> List[Dict]:
        tokenized_query = gold_ex["query"].lower().split()
        scores = self._bm25.get_scores(tokenized_query)

        top_scores = np.argsort(scores)[::-1][:self._n_demonstrations]
        demonstrations = [self._train_examples[i] for i in top_scores]
        return demonstrations
