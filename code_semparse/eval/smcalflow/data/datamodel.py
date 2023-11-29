import ast
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Union

from eval.datamodel_helper import skip, RepresentArgs, RepresentKeywords, RepresentEnum, RepresentEnumValue


# START

@dataclass
class Person:
    name: str

    def func_repr(self):
        return ast.Name(id=self.name)

    @property
    def team(self) -> List["Person"]:
        return [FindTeamOf(self)]

    @property
    def reports(self) -> List["Person"]:
        return [FindReports(self)]

    @property
    def manager(self) -> "Person":
        return FindManager(name=None, recipient=self)

    def find_manager_of(self) -> "Person":
        return FindManager(name=None, recipient=self)

    def find_team_of(self) -> List["Person"]:
        return [FindTeamOf(self)]

    def find_reports_of(self) -> List["Person"]:
        return [FindReports(self)]


@skip
@dataclass
class CurrentUser(Person, RepresentArgs):
    def __init__(self):
        super().__init__(name="CurrentUser ()")

@skip
@dataclass
class FindTeamOf:
    recipient: Person

    def func_repr(self):
        return ast.Call(
            func=ast.Name(id='FindTeamOf'),
            args=[self.recipient.func_repr()],
            keywords=[]
        )


@skip
@dataclass
class FindReports:
    recipient: Person

    def func_repr(self):
        return ast.Call(
            func=ast.Name(id='FindReports'),
            args=[],
            keywords=[ast.keyword(arg='recipient', value=self.recipient.func_repr())]
        )


@skip
@dataclass
class FindManager(Person):
    recipient: Person

    def func_repr(self):
        return ast.Call(
            func=ast.Name(id='FindManager'),
            args=[self.recipient.func_repr()],
            keywords=[]
        )


@dataclass
class Location:
    @staticmethod
    def RoomRequest() -> "Location":
        return RoomRequest()


@skip
class RoomRequest(RepresentArgs):
    _dataflow_name = "roomRequest"


@dataclass
class Event:
    attendees: List[Person] = None
    attendees_to_avoid: List[Person] = None
    subject: Optional[str] = None
    location: Optional[Union[Location, str]] = None
    starts_at: Optional[List["DateTimeClause"]] = None
    ends_at: Optional[List["DateTimeClause"]] = None

    @property
    def ends_at(self) -> List["DateTimeClause"]:
        return EndTimeOfEvent(event=self)

    _ends_at: Optional[List["DateTimeClause"]] = None
    duration: Optional["TimeUnit"] = None
    show_as_status: Optional["ShowAsStatus"] = None
    is_all_day: Optional[bool] = None

    @ends_at.setter
    def ends_at(self, value):
        self._ends_at = value

    def __init__(self, attendees: List[Person] = None, attendees_to_avoid = List[Person], subject: Optional[str] = None, location: Optional[Union[Location, str]] = None, starts_at: Optional[List["DateTimeClause"]] = None, ends_at: Optional[List["DateTimeClause"]] = None, duration: Optional["TimeUnit"] = None, show_as_status: Optional["ShowAsStatus"] = None, is_all_day: Optional[bool] = None):
        self.attendees = attendees
        self.attendees_to_avoid = attendees_to_avoid
        self.subject = subject
        self.location = location
        self.starts_at = starts_at
        self._ends_at = ends_at
        self.duration = duration
        self.show_as_status = show_as_status
        self.is_all_day = is_all_day

    @skip
    def func_repr(self):
        # CreateEvent(with_attendee( John Doe ) )
        with_attendees_args = self.get_event_args()

        return ast.Call(
            func=ast.Name(id='CreateEvent'),
            args=with_attendees_args,
            keywords=[]
        )

    @skip
    def get_event_args(self):
        event_args = []
        for attendee in self.attendees or []:
            if type(attendee) is list:
                # this happens since FindTeamOf/FindReports return a list
                attendee = attendee[0]

            event_args.append(
                ast.Call(
                    func=ast.Name(id='with_attendee'),
                    args=[attendee.func_repr()],
                    keywords=[]
                )
            )
        if self.subject:
            event_args.append(
                ast.Call(
                    func=ast.Name(id='has_subject'),
                    args=[ast.alias(name=self.subject)],
                    keywords=[]
                )
            )
        if self.show_as_status:
            event_args.append(
                ast.Call(
                    func=ast.Name(id='has_status'),
                    args=[self.show_as_status.func_repr()],
                    keywords=[]
                )
            )
        if self.starts_at:
            start_at_clauses = self.starts_at
            if type(self.starts_at) != list:
                start_at_clauses = [self.starts_at]

            for start_at_clause in start_at_clauses:
                event_args.append(
                    ast.Call(
                        func=ast.Name(id='starts_at'),
                        args=start_at_clause.func_repr(),
                        keywords=[]
                    )
                )
        if self._ends_at:
            ends_at_clauses = self._ends_at
            if type(self._ends_at) != list:
                ends_at_clauses = [self._ends_at]

            for ends_at_clause in ends_at_clauses:
                event_args.append(
                    ast.Call(
                        func=ast.Name(id='ends_at'),
                        args=ends_at_clause.func_repr(),
                        keywords=[]
                    )
                )
        if self.duration:
            event_args.append(
                ast.Call(
                    func=ast.Name(id='has_duration'),
                    args=self.duration.func_repr(),
                    keywords=[]
                )
            )
        if self.location:
            event_args.append(
                ast.Call(
                    func=ast.Name(id='at_location'),
                    args=[ast.alias(name=self.location) if type(self.location) == str else self.location.func_repr()],
                    keywords=[]
                )
            )
        if self.is_all_day:
            event_args.append(
                ast.Call(
                    func=ast.Name(id='is_allDay'),
                    args=[],
                    keywords=[]
                )
            )
        if len(event_args) > 1:
            # wrap with AND
            event_args = [ast.Call(
                func=ast.Name(id='AND'),
                args=event_args,
                keywords=[]
            )]
        return event_args


@dataclass
class FindEvents(Event):
    starts_at: Optional[List["DateTimeClause"]] = None
    attendees: Optional[List[Person]] = None
    subject: Optional[str] = None

    def func_repr(self):
        event_repr = Event(attendees=self.attendees, starts_at=self.starts_at, subject=self.subject).get_event_args()
        return ast.Call(
            func=ast.Name(id='FindEvents'),
            args=event_repr,
            keywords=[]
        )


@skip
@dataclass
class NextDOW(RepresentArgs):
    day_of_week: str


DateTimeValues = RepresentEnum("DateTimeValues", [
    "Afternoon", "Breakfast", "Brunch", "Dinner", "Early", "EndOfWorkDay", "Evening", "FullMonthofMonth",
    "FullYearofYear", "LastWeekNew", "Late", "LateAfternoon", "LateMorning", "Lunch", "Morning", "NextMonth",
    "NextWeekend", "NextWeekList", "NextYear", "Night", "Noon", "Now", "SeasonFall", "SeasonSpring", "SeasonSummer", "SeasonWinter",
    "ThisWeek", "ThisWeekend", "Today", "Tomorrow", "Yesterday"
])


class DateTimeClause:
    @staticmethod
    def get_by_value(date_time_value: DateTimeValues) -> "DateTimeClause":
        # find enum by name
        return date_time_value

    @staticmethod
    def get_next_dow(day_of_week: str) -> "DateTimeClause":
        return NextDOW(day_of_week)

    @staticmethod
    def date_by_mdy(month: int = None, day: int = None, year: int = None) -> "DateTimeClause":
        return MDY(month, day, year)

    @staticmethod
    def time_by_hm(hour: int = None, minute: int = None, am_or_pm: str = None) -> "DateTimeClause":
        return HourMinute(hour, minute, am_or_pm)

    @staticmethod
    def on_date_before_date_time(date: "DateTimeClause", time: "DateTimeClause") -> "DateTimeClause":
        return TimeBeforeDateTime(date, time)

    @staticmethod
    def on_date_after_date_time(date: "DateTimeClause", time: "DateTimeClause") -> "DateTimeClause":
        return TimeBeforeDateTime(date, time)

    def around_date_time(self, date_time: "DateTimeClause") -> "DateTimeClause":
        return AroundDateTime(date_time)

class _ShowAsStatusType(Enum):
    def __get__(self, instance, owner):
        @dataclass
        class ShowAsStatus:
            status: _ShowAsStatusType
            def func_repr(self):
                return ast.Call(
                    func=ast.Name(id='ShowAsStatus'),
                    args=[ast.alias(name=self.status)],
                    keywords=[]
                )
        return ShowAsStatus(self.name)

ShowAsStatusType = _ShowAsStatusType("ShowAsStatusType", ["Busy", "OutOfOffice"])

@dataclass
class _ShowAsStatus(RepresentArgs):
    status: ShowAsStatusType


@skip
@dataclass
class EndTimeOfEvent:
    event: Event

    def func_repr(self):
        return [ast.Call(
            func=ast.Name(id=':end'),
            args=[self.event.func_repr()],
            keywords=[]
        )]

TimeUnits = RepresentEnum("TimeUnits", ["Hours", "Minutes", "Days"])
TimeUnitsModifiers = RepresentEnum("TimeUnitsModifiers", ["Acouple", "Afew"])

@dataclass
class TimeUnit:
    number: Optional[int] = None
    unit: Optional[TimeUnits] = None
    modifier: Optional[TimeUnitsModifiers] = None

    def func_repr(self):
        if self.number and self.unit:
            if self.unit.name == TimeUnits.Hours.name:
                return Hours(self.number).func_repr()
            elif self.unit.name == TimeUnits.Minutes.name:
                return Minutes(self.number).func_repr()
            elif self.unit.name == TimeUnits.Days.name:
                return Days(self.number).func_repr()
        if self.modifier:
            return self.modifier.func_repr()


@dataclass
class _TimeUnit:
    number: Optional["Number"] = None

@dataclass
class Hours(_TimeUnit, RepresentArgs):
    _dataflow_name = "toHours"


class Minutes(_TimeUnit, RepresentArgs):
    _dataflow_name = "toMinutes"


class Days(_TimeUnit, RepresentArgs):
    _dataflow_name = "toDays"


class Number(RepresentArgs): ...
class Acouple(Number): ...
class Afew(Number): ...
class Int(Number): ...


@dataclass
class nextDayOfMonth(DateTimeClause, RepresentArgs):
    after_date: DateTimeClause
    day_of_month: int

@dataclass
class HourMinute(DateTimeClause):
    hour: Optional[int] = None
    minute: Optional[int] = None

    # am or pm
    ampm: Optional[str] = "pm"

    def func_repr(self):
        if self.ampm is None:
            self.ampm = "pm"
        return [ast.Call(
            func=ast.Name(id=f'HourMinute{"Am" if self.ampm.lower() == "am" else "Pm"}'),
            args=[],
            keywords=[ast.keyword(arg='hours', value=ast.Name(id=str(self.hour))),
                      ast.keyword(arg='minutes', value=ast.Name(id=str(self.minute)))]
        )]


@dataclass
class MDY(DateTimeClause):
    month: Optional[int] = None
    day: Optional[int] = None
    year: Optional[int] = None

    def func_repr(self):
        if self.year is not None:
            return [ast.Call(
                func=ast.Name(id='MDY'),
                args=[],
                keywords=[ast.keyword(arg='month', value=ast.Name(id=str(self.month))),
                          ast.keyword(arg='day', value=ast.Name(id=str(self.day))),
                          ast.keyword(arg='year', value=ast.Name(id=str(self.year)))]
            )]
        else:
            return [ast.Call(
                func=ast.Name(id='MD'),
                args=[],
                keywords=[ast.keyword(arg='month', value=ast.Name(id=str(self.month))),
                          ast.keyword(arg='day', value=ast.Name(id=str(self.day)))]
            )]


@dataclass
class DateTime(DateTimeClause, RepresentArgs):
    date: DateTimeClause
    time: Optional[DateTimeClause] = None

    _dataflow_name = "DateTime?"


@dataclass
class AroundDateTime(DateTimeClause, RepresentKeywords):
    dateTime: DateTime


@dataclass
class OnDateAfterTime(DateTimeClause, RepresentKeywords):
    date: DateTimeClause
    time: DateTimeClause


@dataclass
class OnDateBeforeTime(DateTimeClause, RepresentKeywords):
    date: DateTimeClause
    time: DateTimeClause


@dataclass
class TimeBeforeDateTime(DateTimeClause, RepresentKeywords):
    date: DateTime
    time: DateTime


@skip
def repr_ast(entity):
    return ast.unparse(entity.func_repr())


class API:
    last_created_event = None

    def find_person(self, name: str) -> "Person":
        return Person(name)

    def get_current_user(self) -> "Person":
        return CurrentUser()

    def add_event(self, event: "Event") -> None:
        self.last_created_event = event

    @staticmethod
    def find_event(attendees: Optional[List[Person]] = None, subject: Optional[str] = None) -> "Event":
        return FindEvents(attendees=attendees, subject=subject)


api = API()


if __name__ == "__main__":
    # attendees = [CurrentUser(), api.find_person("Rory"), api.find_person("Rory").manager,
    #              api.find_person("Rory").manager.manager, CurrentUser().manager]
    # api.add_event(Event(attendees=attendees, subject="dinner", starts_at=[DateTimeClause.get_next_dow("FRIDAY"), MDY(11, 30)]))


    # event = Event(starts_at=MDY(month="FEBRUARY", day=31))
    # print(repr_ast(event))
    #
    # print(createEvent(event))

    # api.add_event(Event(subject="seminar",
    #             starts_at=[MDY(month="MARCH", day=19), DateTimeClause.time_by_hm(hour=8, minute=15, am_or_pm="am"), NextDOW("FRIDAY")],
    #             duration=Hours(1)))

    # api.add_event(Event(subject="seminar",
    #             starts_at=[DateTimeClause.date_by_mdy(month="MARCH", day=19), HourMinute(hour=8, minute=15, ampm="am"), DateTimeClause.get_next_dow("FRIDAY"), DateTimeClause.get_by_value("Afternoon")],
    #             duration=TimeUnit(modifier=TimeUnitsModifiers.Afew)))
    # exp = Event(subject="seminar",
    #             starts_at=[AroundDateTime(dateTime=DateTime(date=MDY(month="MARCH", day=19), time=HourMinute(hour=8, minute=15, ampm="am")))])
    #
    # api.add_event(Event(subject="brunch",
    #             starts_at=[api.find_event(subject="orientation").ends_at],
    #             attendees=[api.find_person("Scotty").team],
    #             show_as_status=ShowAsStatusType.Busy
    #             ))

    # exp = Event(is_all_day=True, location=RoomRequest())
    # exp = Event(attendees=[CurrentUser().manager], starts_at=[NextDOW(day_of_week="Friday"), HourMinute(ampm="am")])

    # Please add lunch from 12 to 2 on Friday the 25 th .
    # attendees = [api.find_person("Shirley")]
    # exp = Event(attendees=attendees, location="the Conference Room", starts_at=[HourMinute(hour=10, minute=30, ampm="am")], ends_at=[HourMinute(hour=12, ampm="pm")])

    # attendees = api.find_person("Lax").team
    # attendees_to_avoid = [api.find_person("Kim")]
    # exp = Event(attendees=attendees, attendees_to_avoid=attendees_to_avoid)

    # date = nextDayOfMonth(DateTimeClauseValue.Today, day_of_month=25)
    # exp = Event(subject="lunch", starts_at=[date, HourMinute(hour=12, ampm="pm")],
    #              ends_at=[date, HourMinute(hour=2, ampm="pm")])

    # attendees = [api.find_person("Elli"), api.find_person("Kim")]
    # attendees.extend(api.find_person("Elli").manager)
    # attendees.extend(api.find_person("Kim").manager)
    # api.add_event(Event(subject="Smash Game Night", attendees=attendees))

    # api.add_event(Event(subject="Call with my team", starts_at=[DateTimeClause.time_by_hm(hour=2, minute=30, am_or_pm="pm")]))
    api.add_event(Event(subject="Lunch Meeting", starts_at=[DateTimeClause.time_by_hm(hour=2)]))
    # api.find_person("Mark").find_manager_of()

    print(repr_ast(api.last_created_event))
