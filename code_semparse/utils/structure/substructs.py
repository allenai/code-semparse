from collections import defaultdict
from itertools import product
from functools import cache

import nltk

get_tuple_size = lambda t: 1 + sum([get_tuple_size(c) for c in t[1]]) if isinstance(t, tuple) else 1


@cache
def all_partitions(size):
    import more_itertools
    return [[len(part) for part in p] for p in more_itertools.partitions(range(size))]


@cache
def partitions(size, n_parts):
    return [p for p in all_partitions(size) if len(p) == n_parts]


def tree_to_tuple(t):
    if isinstance(t, nltk.Tree):
        return (t.label(), tuple([tree_to_tuple(c) for c in t]))
    else:
        return t


def tuple_to_tree(t):
    if isinstance(t, tuple):
        return nltk.Tree(t[0], [tuple_to_tree(c) for c in t[1]])
    else:
        return t


def get_subtrees(t: nltk.Tree, max_size: int, context_type: str = None,
                 path: nltk.Tree = None, node: nltk.Tree = None,
                 result: list[nltk.Tree] = None) -> tuple[list[nltk.Tree], list[nltk.Tree]]:
    assert isinstance(t, nltk.Tree)

    if context_type in ['rule', 'nt'] and (path == None or node == None):
        assert path == None and node == None
        path = node = nltk.Tree(t.label(), [])

    if result == None:
        # result = set()
        result = defaultdict(lambda: 0)

    subtrees = defaultdict(lambda: 0, {(t.label(), tuple()): 1})
    # subtrees = set()
    all_child_trees = []
    for i in range(len(t)):
        if isinstance(t[i], nltk.Tree):
            if context_type == 'rule':
                node[:] = [nltk.Tree(c.label(), []) if isinstance(c, nltk.Tree) else c
                           for c in t]
                c_node = node[i]
            elif context_type == 'nt':
                node[:] = [nltk.Tree(t[i].label(), [])]
                c_node = node[0]
            else:
                c_node = None
            c_trees = get_subtrees(t[i], max_size, context_type,
                                   path, c_node, result)[0]
        else:
            c_trees = [t[i]]
            # c_trees = []
        all_child_trees.append(c_trees)
    for c_sizes in partitions(max_size + len(t) - 1, len(t)):
        c_trees = [[t for t in c_trees if get_tuple_size(t) < c_sz]
                   for c_sz, c_trees in zip(c_sizes, all_child_trees) if c_sz > 1]
        for c_tree_comb in product(*c_trees):
            # subtrees.add(tree_to_tuple(nltk.Tree(t.label(), c_tree_comb)))
            subtrees[(t.label(), c_tree_comb)] += 1
    if context_type in ['rule', 'nt']:
        # subtrees = [tuple_to_tree(st) for st in subtrees]
        for st in subtrees:
            node[:] = tuple_to_tree(st)[:]
            result[tree_to_tuple(path)] += 1
    else:
        result |= subtrees
        # result.update(subtrees)
        # subtrees = [tuple_to_tree(st) for st in subtrees]
    # print(subtrees)

    if node is not None: node[:] = []
    return list(subtrees.keys()), list(result.keys())
