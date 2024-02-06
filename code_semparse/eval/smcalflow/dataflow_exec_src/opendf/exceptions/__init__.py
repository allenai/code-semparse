"""
Package containing possible exceptions.
"""
import logging
import traceback

from eval.smcalflow.dataflow_exec_src.opendf.exceptions.df_exception import DFException

logger = logging.getLogger(__name__)


# parse intentional exception into message, node, [hint]
# for unintentional exception - stop execution and print trace info
def parse_node_exception(ex):
    if isinstance(ex, DFException):
        return ex.message, ex.node, ex.hints, ex.suggestions
    logger.warning('Error - unexpected number of args in exception: %s', ex)
    logger.warning(traceback.format_exc())
    exit(1)


# use re_raise_exc to separate intentionally created exceptions from unintentional ones.
# this can save a lot of grief!
# if it's an exception intentionally created by a node - re-raise the exception, to continue with the dialog
# if it's unintentional - stop and show trace.
def re_raise_exc(ex, node=None):
    if isinstance(ex, list):
        for e in ex:
            if not isinstance(e, DFException):
                logger.warning(traceback.format_exc())
                exit(1)
        ex = e
    if isinstance(ex, DFException):
        if node is not None:
            ex.node = node
        raise ex
    else:
        logger.warning(traceback.format_exc())
        raise RuntimeError(repr(ex))
        # exit(1)
