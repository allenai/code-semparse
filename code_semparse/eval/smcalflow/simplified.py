import re

import ast

from eval.smcalflow.dataflow_exec_src.aws_lex_program_synthesis_calendar.execution.assistant import CalendarAssistant
from eval.smcalflow.dataflow_exec_src.aws_lex_program_synthesis_calendar.execution.run_single_turn import feed_expression
from eval.smcalflow.dataflow_exec_src.opendf.applications.smcalflow.storage import DataEntry
from eval.smcalflow.dataflow_exec_src.opendf.graph.dialog_context import DialogContext

KNOWN_NAMES = ["John Doe", "Jane Doe", "Jon Smith", "Jerry Skinner"]


def find_person_names(dataflow_expression):
    if '"' not in dataflow_expression:
        # add quotes around strings so that it can be parsed
        # e.g. with_attendee( Jon Smith ) -> with_attendee("Jon Smith"), but generally for every multi-word string inside parentheses, and for any number of words
        dataflow_expression = re.sub( r"(?<=[\(,=])\s([^=,()]+)(?=[,\)])", lambda m: f'"{m.group(1).strip()}"', dataflow_expression)
        # support also cases with "equal", e.g. "FindTeamOf( recipient=Abby Gonano )"
        dataflow_expression = re.sub(r"(\=\s*)(\b[^(),]+\b)", lambda m: f'{m.group(1)}"{m.group(2)}"', dataflow_expression)
    # remove ":" from names of functions
    dataflow_expression = re.sub( r":(\w+)\(", "\\1(", dataflow_expression)
    # remove "?" from names of functions
    dataflow_expression = re.sub( r"(\w+)\?\(", "\\1(", dataflow_expression)

    tree = ast.parse(dataflow_expression, mode='eval')

    attendees = []

    # for expressions such as 'do( Let("x0","Isla") ) " output a dict with the key being the variable name and the value being the value
    # e.g. {'x0': 'Isla'}
    variable_assignments = {}
    for node in ast.walk(tree):
        # check if "Let" node
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Let":
            # check if the first argument is a string
            if isinstance(node.args[0], ast.Str):
                # check if the second argument is a string
                if isinstance(node.args[1], ast.Str):
                    variable_assignments[node.args[0].value] = node.args[1].value

    # replace all variable names with their values
    for variable_name, variable_value in variable_assignments.items():
        dataflow_expression = dataflow_expression.replace(f"$ {variable_name}", variable_value)

    tree = ast.parse(dataflow_expression, mode='eval')

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ["with_attendee", "avoid_attendee", "FindManager", "FindReports", "FindTeamOf"] and len(node.args) > 0 and isinstance(node.args[0], ast.Str):
            attendees.append(node.args[0].value)

        # find cases where the call has a keyword recipient="John Doe"
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            for keyword in node.keywords:
                if keyword.arg == "recipient" and isinstance(keyword.value, ast.Str):
                    attendees.append(keyword.value.value)

    return set([attendee.lower() for attendee in attendees])


def anonymize_meeting_subjects(dataflow_expression):
    anon_value = "meeting"
    # replace all values of `has_subject`
    return re.sub(r"has_subject\([^\)]+\)", f"has_subject( {anon_value} )", dataflow_expression)


def normalize_entities(dataflow_expression: str, replace_dict=None, should_anonymize_meeting_subjects: bool = True) -> str:
    # normalize parentheses: after every `(` there should be exactly one space, before every `)` there should be exactly one space
    dataflow_expression = re.sub(r"\([ ]*", "( ", dataflow_expression)
    dataflow_expression = re.sub(r"[ ]*\)", " )", dataflow_expression)
    dataflow_expression = re.sub(r"[ ]*=[ ]*", " = ", dataflow_expression)

    person_names = find_person_names(dataflow_expression)
    if should_anonymize_meeting_subjects:
        dataflow_expression = anonymize_meeting_subjects(dataflow_expression)

    if replace_dict is None:
        replace_dict = {expression_person: known_name for expression_person, known_name in
                        zip(person_names, KNOWN_NAMES)}
    else:
        # replace dict with people not already in the dict
        unused_known_names = [known_name for known_name in KNOWN_NAMES if known_name not in replace_dict.values()]
        for expression_person in person_names:
            if expression_person not in replace_dict:
                replace_dict[expression_person] = unused_known_names.pop(0)

    # replace all person names with known names, starting with the longest names (case insensitive)
    for expression_person, known_name in sorted(replace_dict.items(), key=lambda x: len(x[0]), reverse=True):
        dataflow_expression = re.sub(re.escape(f" {expression_person} "), f" {known_name} ", dataflow_expression, flags=re.IGNORECASE)

    return dataflow_expression, replace_dict


def execute_dataflow(dataflow_expression: str):
    bot = CalendarAssistant()

    bot.reset()
    bot.empty_event_table()
    d_context = DialogContext()
    execution_result = feed_expression(dataflow_expression, d_context, draw_graph=False, show_sql=False,
                                       view_graph=False)
    return CalendarAssistant.events(), execution_result.exceptions


def recurisevly_compare_entries(gold, pred):
    if type(gold) != type(pred):
        return False
    if type(gold) is list:
        assert (type(pred) is list)

        sorted_pred = sorted(pred, key=lambda x: x.unique_identifier())
        sorted_gold = sorted(gold, key=lambda x: x.unique_identifier())

        if len(sorted_pred) != len(sorted_gold):
            return False

        for g, p in zip(gold, pred):
            if not recurisevly_compare_entries(g, p):
                return False
        return True

    # check if subclass of DataEntry
    if issubclass(type(gold), DataEntry):
        gold_attributes = [a for a in dir(gold) if not a.startswith('_') and not callable(getattr(gold, a))]
        pred_attributes = [a for a in dir(pred) if not a.startswith('_') and not callable(getattr(pred, a))]

        if len(gold_attributes) != len(pred_attributes):
            return False

        for attr in gold_attributes:
            if attr not in pred_attributes:
                return False
            if not recurisevly_compare_entries(getattr(gold, attr), getattr(pred, attr)):
                return False

    # handle primitive types
    return gold == pred


def evaluate_smcalflow_simplified(prediction, ex, prompt_method):
    gold_target = ex["simplified"]
    try:
        normalized_prediction, replaced_names = normalize_entities(prediction)
        normalized_gold, _ = normalize_entities(gold_target, replace_dict=replaced_names)

        predicted_entries, exceptions = execute_dataflow(normalized_prediction)
        gold_entries, exceptions = execute_dataflow(normalized_gold)

        # Exceptions with "Suggestion" or "Confirmation" in their names are not considered errors
        exceptions = [e for e in exceptions if "Suggestion" not in e.__class__.__name__ and "Confirmation" not in e.__class__.__name__]
        if len(exceptions) > 0:
            raise Exception(f"Exceptions occured during execution: {exceptions}")

        denotation_accuracy = recurisevly_compare_entries(gold_entries, predicted_entries)

        return {
            "success": True,
            "denotation_accuracy": int(denotation_accuracy),
            "accuracy": int(denotation_accuracy),
            "exact_match": int(prediction == gold_target),
            "execution_error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "denotation_accuracy": 0,
            "accuracy": 0,
            "exact_match": int(prediction == gold_target),
            "execution_error": str(e),
        }
    except:
        return {
            "success": False,
            "denotation_accuracy": 0,
            "accuracy": 0,
            "exact_match": int(prediction == gold_target),
            "execution_error": "Unknown execution error",
        }


if __name__ == "__main__":
    # p = "CreateEvent( AND( with_attendee( John ) , with_attendee( FindManager( John ) ) , has_subject( meeting ) , starts_at( Tomorrow( ) ) , starts_at( NumberAM( 8 ) ) ) )"
    # g = "do( Let( x0 , John ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindManager( $ x0 ) ) , starts_at( Tomorrow( ) ) , starts_at( NumberAM( 8 ) ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)
    #
    # p = "CreateEvent( AND( with_attendee( John ) , with_attendee( FindManager( John ) ) , has_subject( meeting ) , starts_at( Tomorrow( ) ) , starts_at( NumberAM( 8 ) ) ) )"
    # g = "do( Let( x0 , John ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindManager( $ x0 ) ) , starts_at( Tomorrow( ) ) , starts_at( NumberAM( 9 ) ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 0)
    #
    # p = "do( Let( x0 , Abby ) , Let( x1 , Jake ) , CreateEvent( AND( with_attendee( FindTeamOf( recipient= $ x1 ) ) , with_attendee( FindTeamOf( recipient= $ x0 ) ) , with_attendee( $ x0 ) , with_attendee( $ x1 ) ) ) )"
    # g = "do( Let( x0 , Abby ) , Let( x1 , Jake ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindTeamOf( recipient= $ x0 ) ) , with_attendee( $ x1 ) , with_attendee( FindTeamOf( recipient= $ x1 ) ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)
    #
    # p = "CreateEvent( AND( with_attendee( FindManager( Lee ) ) , has_subject( Salary Negotiation ) , starts_at( Tomorrow( ) ) , starts_at( NumberAM( 9 ) ) ) )"
    # g = "do( Let( x0 , Lee ) , CreateEvent( AND( with_attendee( FindManager( $ x0 ) ) , has_subject( Salary Negotiation ) , starts_at( Tomorrow( ) ) , starts_at( NumberAM( 9 ) ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)
    #
    # p = "do( Let( x0 , abby ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindTeamOf( recipient= $ x0 ) ) ) ) )"
    # g = "do( Let( x0 , Abby ) , CreateEvent( with_attendee( OR( $ x0 , FindTeamOf( recipient= $ x0 ) ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 0)
    #
    # p = "CreateEvent( AND( with_attendee( FindTeamOf( recipient= CurrentUser( ) ) ) , has_subject( party ) , avoid_start( Date?( dayOfWeek= Weekend( ) ) ) ) )"
    # g = "CreateEvent( AND( with_attendee( FindTeamOf( recipient= CurrentUser( ) ) ) , starts_at( NotOnWeekend( ) ) , has_subject( party ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 0)

    # p = "CreateEvent(AND(with_attendee(FindTeamOf(recipient=CurrentUser ())), has_subject(Drinks with the team), starts_at(NextDOW(Friday)), starts_at(HourMinutePm(hours=8, minutes=0))))"
    # g = "CreateEvent( AND( with_attendee( FindTeamOf( recipient= CurrentUser( ) ) ) , has_subject( drinks ) , starts_at( NextDOW( FRIDAY ) ) , starts_at( NumberPM( 8 ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)
    #
    # p = "CreateEvent(AND(with_attendee(FindManager(Lee)), has_subject(Salary Negotiation), starts_at(DateTime?(date=Tomorrow(), time=HourMinuteAm(hours=9, minutes=None)))))"
    # g = "CreateEvent( AND( with_attendee( FindManager( Lee ) ) , has_subject( Salary Negotiation ) , starts_at( Tomorrow( ) ) , starts_at( NumberAM( 9 ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)

    # p = "CreateEvent(AND(has_subject(lunch), starts_at(MD(month=MARCH, day=25)), starts_at(HourMinutePm(hours=12, minutes=None)), ends_at(MD(month=MARCH, day=25)), ends_at(HourMinutePm(hours=2, minutes=None))))"
    # g = "do( Let( x0 , DateTime?( date= nextDayOfMonth( Today( ) , 25 ) , time= NumberPM( 12 ) ) ) , CreateEvent( AND( has_subject( lunch ) , starts_at( $ x0 ) , ends_at( AND( GE( $ x0 ) , NumberPM( 2 ) ) ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)  # FAILS!

    # p = "CreateEvent(AND(has_subject(meeting), starts_at(Afternoon()), starts_at(NextDOW(Monday))))"
    # g = "CreateEvent( AND( starts_at( Afternoon( ) ) , starts_at( NextDOW( MONDAY ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)
    #
    # p = "CreateEvent(AND(with_attendee(Annie), with_attendee(Jeri), starts_at(Tomorrow()), starts_at(HourMinutePm(hours=2, minutes=None))))"
    # g = "CreateEvent( AND( starts_at( Afternoon( ) ) , starts_at( NextDOW( MONDAY ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 0)

    # p = "CreateEvent(with_attendee(Robells))"
    # g = "CreateEvent( with_attendee( robells ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)
    #
    # p = "CreateEvent(AND(with_attendee(Abby Gonano), with_attendee(FindTeamOf(recipient=Abby Gonano))))"
    # g = "do( Let( x0 , Abby Gonano ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindTeamOf( recipient= $ x0 ) ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)
    #
    # p = "CreateEvent(AND(with_attendee(Abby Gonano), with_attendee(FindTeamOf(recipient=team)), has_subject(Race)))"
    # g = "do( Let( x0 , Abby Gonano ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindTeamOf( recipient= $ x0 ) ) , has_subject( race ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)
    #
    # p = "CreateEvent(AND(has_subject(volleyball game), starts_at(NextDOW(Monday))))"
    # g = "CreateEvent( AND( with_attendee( FindTeamOf( recipient= CurrentUser( ) ) ) , has_subject( volleyball game ) , starts_at( NextDOW( MONDAY ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 0)
    #
    # p = "CreateEvent(AND(with_attendee(Kim Possible), with_attendee(Elli), with_attendee(FindManager(Kim Possible)), with_attendee(FindManager(Elli)), has_subject(Lunch), starts_at(ThisWeek())))"
    # g = "do( Let( x0 , Kim Possible ) , Let( x1 , Elli ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindManager( $ x0 ) ) , with_attendee( $ x1 ) , with_attendee( FindManager( $ x1 ) ) , has_subject( lunch ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)

    # p = "CreateEvent(AND(with_attendee(FindTeamOf(recipient=CurrentUser ())), has_subject(Team Bonding Event), starts_at(HourMinutePm(hours=8, minutes=None))))"
    # g = "CreateEvent( AND( with_attendee( FindTeamOf( recipient= CurrentUser( ) ) ) , has_subject( team bonding ) , starts_at( TimeAround( NumberPM( 8 ) ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)

    # p = "CreateEvent(AND(has_subject(Rehearsal), starts_at(MD(day=15)), starts_at(HourMinuteAm(hours=8))))"
    # g = "CreateEvent( AND( with_attendee( FindTeamOf( recipient= CurrentUser( ) ) ) , has_subject( rehearsal ) , starts_at( nextDayOfMonth( Today( ) , 15 ) ) , starts_at( NumberAM( 8 ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)

    # p = "CreateEvent(AND(with_attendee(Abby Gonano), with_attendee(Team), has_subject(Abby Gonano Race), starts_at(NextWeekList())))"
    # g = "do( Let( x0 , Abby Gonano ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindTeamOf( recipient= $ x0 ) ) , has_subject( race ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 0)

    # p = "CreateEvent(AND(with_attendee(Abby), with_attendee(Jake), with_attendee(FindTeamOf(recipient=Abby)), with_attendee(FindTeamOf(recipient=Jake))))"
    # g = "do( Let( x0 , Abby ) , Let( x1 , Jake ) , CreateEvent( AND( with_attendee( FindTeamOf( recipient= $ x1 ) ) , with_attendee( FindTeamOf( recipient= $ x0 ) ) , with_attendee( $ x0 ) , with_attendee( $ x1 ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)

    # p = "CreateEvent( AND( has_duration( toMinutes( 30 ) ) , with_attendee( FindManager( Lilly ) ) , starts_at( MD( JULY , 22 ) ) ) )"
    # g = "CreateEvent( AND( with_attendee( FindManager( LIlly ) ) , starts_at( MD( month= JULY , day= 22 ) ) , has_duration( toMinutes( 30 ) ) ) )"
    # assert (evaluate_smcalflow_dataflow(p, {"dataflow": g}, None)["denotation_accuracy"] == 1)

    # events, exceptions = execute_dataflow("( Yield :output ( CreateCommitEventWrapper :event ( CreatePreflightEventWrapper :constraint ( Constraint[Event] :attendees ( AttendeeListHasRecipient :recipient ( Execute :intension ( refer ( extensionConstraint ( RecipientWithNameLike :constraint ( Constraint[Recipient] ) :name # ( PersonName \" Kim \" ) ) ) ) ) ) :start ( ?= ( DateAtTimeWithDefaults :date ( NextDOW :dow # ( DayOfWeek \" SATURDAY \" ) ) :time ( NumberPM :number # ( Number 2 ) ) ) ) :subject ( ?= # ( String \" shopping date \" ) ) ) ) ) )")
    events, exceptions = execute_dataflow('do( Let( x0 , John Doe ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindTeamOf( $ x0 ) ) , has_subject( meeting ) , starts_at( NextDOW( FRIDAY ) ) ) ) )')

    print(events)
