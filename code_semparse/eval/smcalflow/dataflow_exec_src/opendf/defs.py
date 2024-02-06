"""
Holds miscellaneous definitions without any dependencies.
This file should not depend on any other file from this project, except for exceptions.
"""
import datetime
import logging
import os
import sys
import pytz
from eval.smcalflow.dataflow_exec_src.opendf.exceptions.python_exception import SingletonClassException, NoEnvironmentAttributeException

base_types = ['Int', 'Float', 'Str', 'Bool', 'CasedStr', 'String', 'Number']

logger = logging.getLogger(__name__)

LOG_LEVELS = {
    'NOTSET': 0,
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50,

}


def config_log(level='INFO'):
    """
    Configures the logging.
    """
    level = LOG_LEVELS.get(level.upper(), LOG_LEVELS['INFO'])
    logging.basicConfig(
        format="%(message)s",
        level=level,
        handlers=[logging.StreamHandler(sys.stdout)]
    )


class EnvironmentDefinition:
    """
    Class to define values for environment-wide variables.
    """

    __instance = None

    @staticmethod
    def get_instance() -> "EnvironmentDefinition":
        """
        Static access method.

        :return: the database instance
        :rtype: "EnvironmentDefinition"
        """
        if EnvironmentDefinition.__instance is None:
            EnvironmentDefinition.__instance = EnvironmentDefinition()
        return EnvironmentDefinition.__instance

    def __init__(self):
        """
        Create the database class.
        """
        if EnvironmentDefinition.__instance is not None:
            raise SingletonClassException()

        # these options mostly control the drawing, but may have some side effects

        self.show_goal_id = True  # draw goal id marker
        self.show_node_id = True  # draw the id# for each node
        self.show_goal_link = True  # draw a link between goals (this affects image rendering)
        self.show_dialog_id = False  # draw dialogue id
        self.show_node_type = False  # draw node type
        self.show_config = True
        self.show_hints = False  # draw hints (used in dialog_txt)
        # noinspection SpellCheckingInspection
        self.show_sugg = False  # draw suggestions
        self.draw_vert = True  # draw vertically
        self.show_tags = True  # draw tags
        self.show_assign = False  # draw assign labels
        self.show_last_ok = False  # draw marker showing if last turn had exception or not
        self.hide_extra_base = False  # don't draw leaf types
        self.show_view = False  # draw view type
        self.show_nodes = True  # turns off drawing of nodes (drawing only text)
        self.show_prm_tags = False  # draw parameter tags (depracated)
        self.show_detach = False  # draw detached nodes (depracated)
        self.show_dup = False  # draw pointers from duplicated nodes to they original nodes
        self.show_sexp = False  # drae S-exp
        self.show_txt = True  # draw text
        self.show_simp = True  # draw simplified text
        self.show_explain = True  # draw explanations
        self.show_only_n = 3  # draw only last N goals (if 0, draw all)
        self.show_alias = True  # draw alias names
        self.hide_internal_db = False  # don't draw nodes internal to the DB - draw only top node from DB(reduce
        # clutter)
        self.sep_graphs = True  # draw each turn in a separate box
        self.show_SQL = False  # draw the SQL message

        self.clear_exc_each_turn = True  # clear exceptions each turn
        self.clear_msg_each_turn = True  # clear messages each turn
        # noinspection SpellCheckingInspection
        self.show_dbg_constr = True  # adds extra nodes to the graph (and draw them) which are helpful for debugging
        self.show_dbg_event = True  # adds extra nodes to the graph (and draw them) which are helpful for debugging

        self.repr_down = True  # this controls Node.__repr__ - how a node is printed: up or down

        self.turn_by_turn = False  # draw turn by turn

        # name of a class that inherits from EventFactory,
        # e.g. SimpleEventFactory, IteratorEventFactory, DatabaseEventFactory, DatabaseStartDurationEventFactory
        self.event_factory_name = "DatabaseStartDurationEventFactory"

        # summarize these types - show the result of their 'describe' instead of drawing their input graphs
        # noinspection SpellCheckingInspection
        # self.summarize_typenames = []  # ['Date', 'WeatherTable', 'Recipient', 'TimeSlot']  # 'Attendee'
        self.summarize_typenames = ['Date', 'WeatherTable', 'Recipient', 'TimeSlot', 'Attendee']  #
        # e.g. ['Recipient', 'Time', 'Date', "DateTime", "TimeSlot", "LocationKeyphrase", "Attendee"]

        # noinspection SpellCheckingInspection
        self.simp_add_interm_goals = True
        # add intermediate simplified graphs as goals (in simplify) - turn on for debug/display

        self.simp_add_init_goal = True  # add initial (original) graph as goal (in simplify) - turn on for debug/display

        self.radius_constraint = 10000
        # the radius constraint to consider where searching for places near another place, in meters

        self.event_fallback_force_curr_user = False

    def update_values(self, **kwargs):
        """
        Updates the values of the variables based on the `kwargs`.

        If the original value of the attribute is a list AND the `value` is a string; the new value will be
        `value.split(",")`. Where `value` is the value of the attribute in `kwargs`.

        :param kwargs: the new values for the variables
        :type kwargs: Dict[str, Any]
        """
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise NoEnvironmentAttributeException(self.__class__.__name__, key)
            original_value = getattr(self, key)
            if isinstance(original_value, list) and isinstance(value, str):
                value = value.split(",")
            elif isinstance(original_value, bool):
                value = value.lower() == "true"
            elif isinstance(original_value, int):
                value = int(value)
            elif isinstance(original_value, float):
                value = float(value)

            setattr(self, key, value)


# The database definition and the system date are used too early in the code, modifying it during the CLI argument
# parsing would be too late
# TODO: use the these variables only after CLI arguments are parsed
use_database = True
# database_connection = "sqlite+pysqlite:///:memory:"  # use this for in memory database
database_connection = f"sqlite+pysqlite:///data/database/{os.getenv('OPENDF_DB_FILENAME', 'test.db')}"
# database_connection = "postgresql://postgres:root@localhost:5432/test"
# in order to use postgres, update this variable to conform with your database installation

database_log = False
database_future = True

# The values below defines the searching space for the database based event factories, changing this values may
# dramatically change the event suggestion runtime, when using these factories
# DatabaseEventFactory
event_suggestion_period = 60  # the number of days, after SYSTEM_DATE, to be considered as suggestions
minimum_slot_interval = 5  # the number of minutes between possible start/end timeslots, e.g. if set to 5,
# only events where the `m % 5 == 0` will be possible, where `m` is the minute of the start (or end) of the event
# when searching DB for events, limit to events with current user

# DatabaseStartDurationEventFactory
minimum_duration = 5  # the minimal possible duration of an event, in minutes
maximum_duration_days = 1  # the maximum duration of an event, in days

# Option to set a specific date for the system
# SYSTEM_DATE = datetime.datetime.today().date()
# SYSTEM_DATE = datetime.date(year=2022, month=1, day=3)
SYSTEM_DATE = datetime.date(year=2022, month=8, day=23)
SYSTEM_TIME = datetime.time(hour=8)

if os.getenv('OPENDF_USE_CLOCK') in ('true', 'yes', '1'):
    SYSTEM_DATE = None
    SYSTEM_TIME = None

TAG_NO_COPY = '//'
TAG_NO_SHOW = '^^'
TAG_NO_MATCH = '&&'
TAG_NO_NO_NO = TAG_NO_COPY + TAG_NO_SHOW + TAG_NO_MATCH

SUGG_LABEL = '?:?'  # suggestion label
SUGG_MSG = '//'  # suggestion message
SUGG_IMPL_AGR = '**'  # suggestion as implicit agreement

CONT_TURN = '||'

TAG_ORIG = TAG_NO_COPY + 'org'
MOD_CONV1 = TAG_NO_SHOW + 'conv'  # conv once
# noinspection SpellCheckingInspection
MOD_RECONV = TAG_NO_SHOW + TAG_NO_COPY + 'conv'  # reconvert per copy

MSG_COL = '*??*'
MSG_YELLOW = MSG_COL + '#ffff00'
MSG_YIELD = MSG_COL + '#ff44aa'
MSG_GREEN = MSG_COL + '#00ff00'
MSG_SQL = MSG_COL + '#aaccaa'

OUTLINE_COLOR = TAG_NO_NO_NO + '_out'  # prefix for node outline color - does not get copied, displayed, or matched
OUTLINE_GRAY1 = OUTLINE_COLOR + '#aaaaaa'
OUTLINE_BLACK = OUTLINE_COLOR + '#000000'
OUTLINE_SIMP = OUTLINE_COLOR + '#0000ff'  # for marking simplified expansion

NODE_COLOR = TAG_NO_NO_NO + '_node'
NODE_COLOR_DB = NODE_COLOR + '#ccddcc'

WRAP_COLOR_TAG = [NODE_COLOR + '#ddddaa', OUTLINE_COLOR + '#888866']  # mark automatically added input nodes
RES_COLOR_TAG = [OUTLINE_GRAY1, NODE_COLOR + '#ccccee']

only_one_exception = False  # context keeps only the last exception
unique_exception = True  # if not uniq - then same node can have the same exception happen again
#     this can happen if a node which threw an exception is used again in a new graph
DB_NODE_TAG = TAG_NO_SHOW + TAG_NO_COPY + 'db_node'

#  NODE = ['Any', 'Node']  # synonymous type names for Node

OVERRIDE_EXC = ['Exists', 'size']  # nodes which ignore exceptions thrown under them

BLOCK_TRAVERSE = ['BLOCK']

VIEW_INT = 1  # intension
VIEW_EXT = 2  # extension

MULT_NO = 0
MULT_ALREADY = 1
MULT_POSSIBLE = 2

# noinspection SpellCheckingInspection
tagmark = '^'

# noinspection SpellCheckingInspection
DEBUG_MSG = 'DBGMSG'  # marks a string value for special formatting when drawing graph

# special names for automatic variables. Defining like this make it easy to change these names later if needed
POS = 'pos'

VERBOSE = False
ALWAYS_FOUND_EVENT = False
ALWAYS_FOUND_RECIPIENT = False


def get_system_date():
    """
    Gets the system's current date, as defined in `SYSTEM_DATE`.

    :return: the system's current date
    :rtype: datetime.date
    """
    if SYSTEM_DATE:
        return SYSTEM_DATE
    else:
        return datetime.datetime.now(tz=get_system_timezone())


def get_system_timezone():
    tz = os.getenv('OPENDF_TIMEZONE', None)
    if tz:
        try:
            tz = pytz.timezone(tz)
        except:
            tz = None
    return tz


def get_system_datetime():
    """
    Gets the system's current date and time, as defined in `SYSTEM_DATE`.

    :return: the system's current datetime
    :rtype: datetime.datetime
    """
    date = get_system_date()
    time = SYSTEM_TIME
    if not time:
        time = datetime.datetime.now(tz=get_system_timezone())
    return datetime.datetime(date.year, date.month, date.day, time.hour, time.minute, time.second, time.microsecond)


def is_pos(s):
    return s.startswith(POS) and s[len(POS):].isnumeric()


def posname(i):
    return POS + '%d' % i


def posname_idx(s):
    return int(s[len(POS):]) if is_pos(s) else 0


def show_prm_nm(i, with_pos):
    if is_pos(i) and not with_pos:
        return ''
    return i + '='
