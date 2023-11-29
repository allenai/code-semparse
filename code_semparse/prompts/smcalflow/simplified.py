structures = {
    "list_of_operators": """```
FindTeamOf
FindReports
FindManager

with_attendee
avoid_attendee
has_subject
at_location
starts_at
ends_at
has_duration
has_status

Afternoon
Breakfast
Brunch
Dinner
Early
EndOfWorkDay
Evening
FullMonthofMonth
FullYearofYear
LastWeekNew
Late
LateAfternoon
LateMorning
Lunch
Morning
NextMonth
NextWeekend
NextWeekList
NextYear
Night
Noon
Now
SeasonFall
SeasonSpring
SeasonSummer
SeasonWinter
ThisWeek
ThisWeekend
Today
Tomorrow
Yesterday

DateTime
Date
DayOfWeek
NextDOW
MD
MDY

toMonth
toFourDigitYear
HourMinuteAm
HourMinutePm
NumberAM
NumberPM

OnDateAfterTime
OnDateBeforeTime
AroundDateTime

toDays
toHours
toMinutes

Acouple
Afew

ShowAsStatus

CreateEvent
FindEvents
CurrentUser

do
Let

AND
```""",
    "full_dd": """```
FindTeamOf  # given a person name or id, returns a pseudo-person representing the team of that person
FindReports  # given a person name or id, returns a pseudo-person representing the reports of that person
FindManager  # given a person name or id, returns the manager of that person

with_attendee  # given a person name or id, returns a clause to match or create an event with that person as an attendee
avoid_attendee  # given a person name or id, returns an event clause to avoid that attendee when creating an event
has_subject  # given a string, returns an event to match or create an event with that subject
at_location  # given a string, returns an event clause to match or create an event at that location
starts_at  # given a datetime clause, returns an event clause to match or create an event starting at that time
ends_at  # given a datetime clause, returns an event clause to match or create an event ending at that time
has_duration  # given a time unit value, returns an event clause to match or create an event with that duration
has_status  # given a ShowAsStatus value, returns an event clause to match or create an event with that status

# the following operators return datetime clauses and accept no arguments
Afternoon
Breakfast
Brunch
Dinner
Early
EndOfWorkDay
Evening
FullMonthofMonth
FullYearofYear
LastWeekNew
Late
LateAfternoon
LateMorning
Lunch
Morning
NextMonth
NextWeekend
NextWeekList
NextYear
Night
Noon
Now
SeasonFall
SeasonSpring
SeasonSummer
SeasonWinter
ThisWeek
ThisWeekend
Today
Tomorrow
Yesterday

# general date time clauses
DateTime  # given either a datetime clause representing a date and/or a time operator representing a time, returns a datetime clause
Date  # given a date or dayofweek, returns a date
DayOfWeek  # given a day of week string, returns a time clause
NextDOW  # given a day of week string, returns a time clause for the next occurrence of that day of week
MD  # given a month and day as arguments, returns a date clause
MDY  # given a month, day, and year as arguments, returns a date clause

# given a value, the following operators return datetime clauses according to the given value
toMonth
toFourDigitYear
HourMinuteAm
HourMinutePm
NumberAM
NumberPM

# given a datetime clause, the following operators modify the clause and return a datetime clause according to the modification
OnDateAfterTime
OnDateBeforeTime
AroundDateTime

# given either a number or the operators Acouple/Afew, all the following operators return time unit values according to the given unit
toDays
toHours
toMinutes

# these operators can be used to create time unit values instead of using integer values
Acouple
Afew

ShowAsStatus  # enumeration of possible event statuses (Busy, OutOfOffice)

CreateEvent  # given multiple event clauses (such as with_attendee, has_subject, combined together with `AND`), creates an event complying with those clauses
FindEvents  # given multiple event clauses (such as with_attendee, has_subject, combined together with `AND`), returns a list of events complying with those clauses
CurrentUser  # returns the current user (person)

do  # allows the execution of multiple commands in a single prompt (each command is an argument). Often used in conjunction with `Let` to define variables
Let  # defines a variable (first argument) with a value (second argument)

AND  # combines multiple event clauses together
```"""}
solution_prefix = ""
test_solution_prefix = ""
