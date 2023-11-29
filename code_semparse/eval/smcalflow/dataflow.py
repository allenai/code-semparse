from eval.smcalflow.dataflow_exec_src.aws_lex_program_synthesis_calendar.execution.run_single_turn import init_node_factory
from eval.smcalflow.dataflow_exec_src.opendf.defs import OUTLINE_SIMP
from eval.smcalflow.dataflow_exec_src.opendf.dialog_simplify import prep_turn
from eval.smcalflow.dataflow_exec_src.opendf.graph.constr_graph import construct_graph
from eval.smcalflow.dataflow_exec_src.opendf.graph.dialog_context import DialogContext
from eval.smcalflow.dataflow_exec_src.opendf.graph.simplify_graph import pre_simplify_graph, simplify_graph, clean_operators
from eval.smcalflow.simplified import evaluate_smcalflow_simplified

d_context = DialogContext()
d_context.suppress_exceptions = True  # avoid exit in


def simplify_smcalflow(lispress_expression):
    """The following code is based on `opendf/dialog_simplify.py`. Since original code accepts an entire file,
    here we accept a single expression and return the simplified expression."""
    init_node_factory(for_simplification=True)

    isexp, org = prep_turn(lispress_expression)
    igl, ex = construct_graph(isexp, d_context, constr_tag=OUTLINE_SIMP, no_post_check=True, no_exit=True)

    bgl, ex = pre_simplify_graph(igl, d_context)

    gl, ex = simplify_graph(bgl, d_context)

    if 'let' in isexp:
        gl, ex = simplify_graph(gl, d_context)

    clean_operators(gl)
    gl.reorder_inputs_recurr()
    d_context.add_goal(gl)

    simp, _ = gl.print_tree(None, ind=None, with_id=False, with_pos=False,
                            trim_leaf=True, trim_sugar=True, mark_val=True)

    return simp


def evaluate_smcalflow_dataflow(prediction, ex, prompt_method, simplify=True):
    # first convert python to simplified dataflow since we can execute it, then evaluate
    gold_target = ex["dataflow"]

    if simplify:
        try:
            simplified_exp = simplify_smcalflow(prediction).replace('"', '')
        except Exception as e:
            return {
                "success": True,
                "denotation_accuracy": 0,
                "accuracy": 0,
                "exact_match": int(prediction == gold_target),
                "error": str(e),
            }
    else:
        simplified_exp = prediction
    eval_results = evaluate_smcalflow_simplified(simplified_exp, ex, prompt_method)
    eval_results["converted_dataflow"] = simplified_exp
    eval_results["exact_match"] = eval_results["exact_match"] or int(prediction == gold_target)

    return eval_results


if __name__ == "__main__":
    exp = '( Yield :output ( CreateCommitEventWrapper :event ( CreatePreflightEventWrapper :constraint ( Constraint[Event] :attendees ( andConstraint ( AttendeeListHasRecipient :recipient ( Execute :intension ( refer ( extensionConstraint ( RecipientWithNameLike :constraint ( Constraint[Recipient] ) :name # ( PersonName " Ryan " ) ) ) ) ) ) ( AttendeeListHasRecipientConstraint :recipientConstraint ( FindManager :recipient ( Execute :intension ( refer ( extensionConstraint ( RecipientWithNameLike :constraint ( Constraint[Recipient] ) :name # ( PersonName " Ryan " ) ) ) ) ) ) ) ) ) ) ) )'
    simplified = simplify_smcalflow(exp)

    print(simplified)
