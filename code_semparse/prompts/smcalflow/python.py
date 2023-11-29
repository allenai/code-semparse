structures = {"full_dd": """```python
@dataclass
class Person:
    name: str
    
    def find_team_of() -> List["Person"]:
        ...
    
    def find_reports_of() -> List["Person"]:
        ...
    
    def find_manager_of() -> "Person":
        ...

@dataclass
class Event:
    attendees: List[Person] = None
    attendees_to_avoid: List[Person] = None
    subject: Optional[str] = None
    location: Optional[str] = None
    starts_at: Optional[List[DateTimeClause]] = None
    ends_at: Optional[List[DateTimeClause]] = None
    duration: Optional["TimeUnit"] = None
    show_as_status: Optional["ShowAsStatus"] = None

DateTimeValues = Enum("DateTimeValues", ["Afternoon", "Breakfast", "Brunch", "Dinner", "Early", "EndOfWorkDay", "Evening",
    "FullMonthofMonth", "FullYearofYear", "LastWeekNew", "Late", "LateAfternoon", "LateMorning", "Lunch", "Morning",
    "NextMonth", "NextWeekend", "NextWeekList", "NextYear", "Night", "Noon", "Now", "SeasonFall", "SeasonSpring",
    "SeasonSummer", "SeasonWinter", "ThisWeek", "ThisWeekend", "Today", "Tomorrow", "Yesterday"])

class DateTimeClause:
    def get_by_value(date_time_value: DateTimeValues) -> "DateTimeClause": ...
    def get_next_dow(day_of_week: str) -> "DateTimeClause": ...
    def date_by_mdy(month: int = None, day: int = None, year: int = None) -> "DateTimeClause": ...
    def time_by_hm(hour: int = None, minute: int = None, am_or_pm: str = None) -> "DateTimeClause": ...
    def on_date_before_date_time(date: "DateTimeClause", time: "DateTimeClause") -> "DateTimeClause": ...
    def on_date_after_date_time(date: "DateTimeClause", time: "DateTimeClause") -> "DateTimeClause": ...
    def around_date_time(date_time: "DateTimeClause") -> "DateTimeClause": ...


TimeUnits = Enum("TimeUnits", ["Hours", "Minutes", "Days"])
TimeUnitsModifiers = Enum("TimeUnitsModifiers", ["Acouple", "Afew"])

@dataclass
class TimeUnit:
    number: Optional[Union[int,float]] = None
    unit: Optional[TimeUnits] = None
    modifier: Optional[TimeUnitsModifiers] = None

ShowAsStatusType = Enum("ShowAsStatusType", ["Busy", "OutOfOffice"])
    

class API:
    def find_person(name: str) -> Person:
        ...
    
    def get_current_user() -> Person:
        ...

    def add_event(event: Event) -> None:
        ...

    def find_event(attendees: Optional[List[Person]] = None, subject: Optional[str] = None) -> Event:
        ...

api = API()
```""", "no_typing": """```python
@dataclass
class Person:
    name
    
    def find_team_of():
        ...
    
    def find_reports_of():
        ...
    
    def find_manager_of():
        ...

@dataclass
class Event:
    attendees = None
    attendees_to_avoid = None
    subject = None
    location = None
    starts_at = None
    ends_at = None
    duration = None
    show_as_status = None

DateTimeValues = Enum("DateTimeValues", ["Afternoon", "Breakfast", "Brunch", "Dinner", "Early", "EndOfWorkDay", "Evening",
    "FullMonthofMonth", "FullYearofYear", "LastWeekNew", "Late", "LateAfternoon", "LateMorning", "Lunch", "Morning",
    "NextMonth", "NextWeekend", "NextWeekList", "NextYear", "Night", "Noon", "Now", "SeasonFall", "SeasonSpring",
    "SeasonSummer", "SeasonWinter", "ThisWeek", "ThisWeekend", "Today", "Tomorrow", "Yesterday"])

class DateTimeClause:
    def get_by_value(date_time_value): ...
    def get_next_dow(day_of_week): ...
    def date_by_mdy(month = None, day = None, year = None): ...
    def time_by_hm(hour = None, minute = None, am_or_pm = None): ...
    def on_date_before_date_time(date, time): ...
    def on_date_after_date_time(date, time): ...


TimeUnits = Enum("TimeUnits", ["Hours", "Minutes", "Days"])
TimeUnitsModifiers = Enum("TimeUnitsModifiers", ["Acouple", "Afew"])

@dataclass
class TimeUnit:
    number = None
    unit = None
    modifier = None

ShowAsStatusType = Enum("ShowAsStatusType", ["Busy", "OutOfOffice"])
    

class API:
    def find_person(name):
        ...
    
    def get_current_user():
        ...

    def add_event(event):
        ...

    def find_event(attendees = None):
        ...

api = API()
```""", "list_of_operators": """```python
Person
find_team_of
find_reports_of
find_manager_of

Event
attendees
attendees_to_avoid
subject
location
starts_at
ends_at
duration
show_as_status

DateTimeClause
get_by_value
Afternoon, Breakfast, Brunch, Dinner, Early, EndOfWorkDay, Evening, FullMonthofMonth, FullYearofYear, LastWeekNew,
Late, LateAfternoon, LateMorning, Lunch, Morning, NextMonth, NextWeekend, NextWeekList, NextYear, Night, Noon, Now,
SeasonFall, SeasonSpring, SeasonSummer, SeasonWinter, ThisWeek, ThisWeekend, Today, Tomorrow, Yesterday

get_next_dow
date_by_mdy
time_by_hm
on_date_before_date_time
on_date_after_date_time


TimeUnits
TimeUnitsModifiers

TimeUnit
number
unit
modifier

ShowAsStatusType
    
API
find_person
get_current_user
add_event
find_event
```"""}

solution_prefix = ""
test_solution_prefix = ""
