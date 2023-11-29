import re
from collections import defaultdict

from tqdm import tqdm

from utils.structure.ast_parser import target_to_ast
from utils.structure.substructs import get_subtrees


def simple_extract_atoms(program):
    # find all atoms using regex, e.g. from FindTeamOf( recipient= with_attendee( Jesse ) ) we get ['FindTeamOf', 'recipient', 'with_attendee', 'Jesse']
    atoms = set(re.findall(r'\w+', program))

    # skip number-only atoms
    atoms = [atom for atom in atoms if not atom.replace(".", "").isdigit()]

    return atoms


def get_lfsubtrees(targets, max_size, context_type, verbose=True):
    all_subtrees = set()
    subtree2ex = defaultdict(list)
    ex2subtree = []
    for qid, target in enumerate(tqdm(targets, desc="Extracting LF subtrees", disable=not verbose)):
        tree = target_to_ast(target)
        _, ex_subtrees = get_subtrees(tree, max_size, context_type)
        ex2subtree.append(ex_subtrees)
        for subtree in ex_subtrees:
            all_subtrees.add(subtree)
            subtree2ex[subtree].append(qid)
    # print(f'{len(all_subtrees)} subtrees with max size {max_size} and context type {context_type}')
    # all_subtrees = [tuple_to_tree(st) for st in all_subtrees]
    # return {k: dict(v) for k, v in subtree2ex.items()}, ex2subtree
    return dict(subtree2ex), ex2subtree


def get_substructs(strings, substruct, subst_size, depparser='spacy', parser=None, verbose=False, prompt_lang=None):
    # if prompt_lang == "python":
    #     assert subst_size == 1
    #     str2struct = [simple_extract_atoms(s) for s in strings]
    # else:
    _, str2struct = get_lfsubtrees(strings, subst_size, None, verbose=verbose)
    str2struct = [sorted(list(set(d))) for d in str2struct]
    return str2struct
