import numpy as np


def recall_stscores_v3(query_structs, cand_structs):
    cand_stscores = np.array([[1 / len(query_structs) if s in _cand_structs else 0 for s in query_structs] for _cand_structs in cand_structs])
    return cand_stscores


def bm25_stscores_v2(query_structs, bm25):
    doc_len = np.array(bm25.doc_len)

    def cand_stscore(q):
        q_freq = np.array([(doc.get(q) or 0) for doc in bm25.doc_freqs])
        score = (bm25.idf.get(q) or 0) * (q_freq * (bm25.k1 + 1) /
                                          (q_freq + bm25.k1 * (1 - bm25.b + bm25.b * doc_len / bm25.avgdl)))
        return score

    cand_stscores = np.array([cand_stscore(s) for s in query_structs]).T
    return cand_stscores