from eval.smcalflow.dataflow_exec_src.aws_lex_program_synthesis_calendar.benchmark.evaluation import TurnPrediction
from eval.smcalflow.dataflow_exec_src.aws_lex_program_synthesis_calendar.execution.assistant import CalendarAssistant
from eval.smcalflow.dataflow_exec_src.aws_lex_program_synthesis_calendar.execution.run_single_turn import init_node_factory, feed_expression
from eval.smcalflow.dataflow_exec_src.aws_lex_program_synthesis_calendar.sub_data import example_database as data
from eval.smcalflow.dataflow_exec_src.opendf.applications.smcalflow.database import populate_stub_database
from eval.smcalflow.dataflow_exec_src.opendf.exceptions.python_exception import UnknownNodeTypeException
from eval.smcalflow.dataflow_exec_src.opendf.graph.dialog_context import DialogContext

# EXPRESSION = "CreateEvent( AND( has_subject( quitting time ) , starts_at( Today( ) ) , starts_at( NumberPM( 4 ) ) ) )"
EXPRESSION = "FindManager( Jon Smith )"


def execute_turn(bot, expression):
    bot.reset()
    bot.empty_event_table()
    d_context = DialogContext()
    result = feed_expression(expression, d_context, draw_graph=False,
                             save_path='data/visualization/bot_cli.pdf',
                             show_sql=False, view_graph=False)
    return TurnPrediction(expression=expression, agent_response=result.agent_response, events=CalendarAssistant.events())


if __name__ == '__main__':
    # init_node_factory()

    bot = CalendarAssistant()

    turn = execute_turn(bot, EXPRESSION)

    # d_context.suppress_exceptions = True  # avoid exit in
    # bot.talk(expression=expression, force_confirm=True)
    # print(result.agent_response)
    a = 1
