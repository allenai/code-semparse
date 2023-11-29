"""
Collect Node type related information here and store in a format which can be passed to a function which does not have
to directly know anything about the node types.
"""

# must import opendf.applications.smcalflow.nodes.functions, so all_nodes can work properly
from eval.smcalflow.dataflow_exec_src.opendf.applications.smcalflow.nodes.functions import *
from eval.smcalflow.dataflow_exec_src.opendf.graph.nodes.framework_functions import *
from eval.smcalflow.dataflow_exec_src.opendf.utils.utils import get_subclasses
from eval.smcalflow.dataflow_exec_src.opendf.applications.sandbox.sandbox import *

def fill_type_info(node_factory, all_nodes=None, for_simplification: bool = False):
    """
    Fills the node types to the node factory.

    :param node_factory: the node factory
    :type node_factory: NodeFactory
    """
    # node_types: dictionary  name -> node type
    # all_nodes = Node.__subclasses__()     # this adds only one level of subclasses
    if not all_nodes:
        all_nodes = list(get_subclasses(Node))  # add recursively inherited nodes

    # hack to separate simplification nodes and actual nodes
    if for_simplification:
        node_types = {t.__name__: t for t in all_nodes}
    else:
        node_types = {t.__name__: t for t in all_nodes if 'simplification' not in t.__module__}

    # node_types['Any'] = Node  # 'Any' is a synonym for 'Node'
    node_types['Node'] = Node
    node_factory.node_types = node_types  # fill node_fact BEFORE making sample nodes

    # sample nodes: dictionary name -> instance of a node of that type
    if for_simplification:
        sample_nodes = {t.__name__: t() for t in all_nodes}
    else:
        sample_nodes = {t.__name__: t() for t in all_nodes if 'simplification' not in t.__module__}
    # sample_nodes['Any'] = Node()
    sample_nodes['Node'] = Node()
    node_factory.sample_nodes = sample_nodes

    node_factory.set_leaf_types()
    node_factory.init_lists()
