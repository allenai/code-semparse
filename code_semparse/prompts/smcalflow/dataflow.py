structures = {
    "list_of_operators": """```
    Yield
CreateCommitEventWrapper 
CreatePreflightEventWrapper
FindEventWrapperWithDefaults

extensionConstraint
Constraint[Event]
Constraint[DateTime]
andConstraint
RecipientWithNameLike
PersonName
AttendeeListHasRecipient
AttendeeListHasPeople
AttendeeListHasRecipientConstraint
DateTimeConstraint
AttendeeListExcludesRecipient

Execute
refer
singleton
do
String

FindManager
FindReports
FindTeamOf
toRecipient
CurrentUser

LocationKeyphrase
roomRequest

Today
Tomorrow
NextWeekList
NextDOW
Noon
Afternoon
Morning
Night
EndOfWorkDay
Evening
Weekend
ThisWeekend
ThisWeek
Early
Now
NextYear
Lunch

Number
NumberAM
NumberPM
toDays
toHours
toMinutes

DateAndConstraint
DateAtTimeWithDefaults
nextDayOfMonth
DayOfWeek
DowOfWeekNew
previousDayOfWeek
NextDOW
EventAllDayStartingDateForPeriod
PeriodDuration

MD
MDY
Month
NextTime
HourMinuteAm
HourMinutePm
FullMonthofMonth

TimeAfterDateTime
OnDateAfterTime
AroundDateTime
```""",
    "full_dd": """```
Yield  # Arguments: (1) :output, the function to be executed. Returns: The result of the function.
CreateCommitEventWrapper   # Arguments: (1) :event, containing event details. Returns: The created event.
CreatePreflightEventWrapper  # Arguments: (1) :constraint, containing event details. Returns: The event that satisfies the constraint.
FindEventWrapperWithDefaults  # Arguments: (1) :constraint, the constraint to be satisfied by the event. Returns: The event that satisfies the constraint.

extensionConstraint  # Arguments: (1) the type of constraint (e.g., Constraint[Recipient], Constraint[Date], RecipientWithNameLike), Returns: A constraint that needs to be satisfied by the entity.
Constraint[Event]  # Arguments: (1) :attendees, :start, :subject or :location. Returns: Constraints to create or find an event.
Constraint[DateTime]  # Arguments: (1) :date, the date constraint. Returns: A constraint that needs to be satisfied by the date and time.
andConstraint  # Arguments: Any number of constraints. Returns: A constraint that is satisfied when all the input constraints are satisfied.
RecipientWithNameLike  # Arguments: (1) :constraint, the type of constraint (e.g., Constraint[Recipient]), (2) :name, the name of the recipient. Returns: A constraint that needs to be satisfied by the recipient.
PersonName  # Arguments: (1) the name of the person. Returns: The name of the person. e.g. `PersonName " Dan "`  
AttendeeListHasRecipient  # Arguments: (1) :recipient, the recipient to be included. Returns: A constraint for the event.
AttendeeListHasPeople  # Arguments: (1) :people, the group of people to be included. Returns: A constraint for the event.
AttendeeListHasRecipientConstraint  # Arguments: (1) :recipientConstraint, the recipient constrained to be included. Returns: A constraint for the event.
DateTimeConstraint  # Arguments: (1) :constraint, the time constraint, (2) :date, the date. Returns: A constraint that needs to be satisfied by the date and time.
AttendeeListExcludesRecipient  # Arguments: (1) :recipient, the recipient to be excluded. Returns: A constraint for the event.

Execute  # Arguments: (1) :intension, the intension to be executed. Returns: The entity referred to by the intension.
refer  # Arguments: (1) extensionConstraint, the constraint to be satisfied by the entity. Returns: A reference to the entity that satisfies the constraint.
singleton  # Arguments: (1) an element or a list with an element. Returns: The single element.
do  # Arguments: Any number of functions. Returns: The results of the functions.
String  # Arguments: (1) a literal string. Returns: A string representation.

FindManager  # Arguments: (1) :recipient, the recipient whose manager is to be found. Returns: The manager of the recipient.
FindReports  # Arguments: (1) :recipient, the recipient whose reports are to be found. Returns: The reports of the recipient.
FindTeamOf  # Arguments: (1) :recipient, the recipient whose team is to be found. Returns: The group of people who make up the recipient's team.
toRecipient  # Arguments: (1) A user. Returns: The given user as a recipient.
CurrentUser  # Arguments: None. Returns: The current user.

LocationKeyphrase  # Arguments: (1) the location. Returns: The location. e.g. `LocationKeyphrase " office "`  
roomRequest  # Arguments: None. Returns: A request for a room.

# These operators represent specific times or dates. They have no arguments and return the specified time or date.
Today
Tomorrow
NextWeekList
NextDOW
Noon
Afternoon
Morning
Night
EndOfWorkDay
Evening
Weekend
ThisWeekend
ThisWeek
Early
Now
NextYear
Lunch

# These operators represent specific numbers or convert values to numbers. Arguments: (1) the number or value to be converted. Returns: The specific number or the converted value.
Number
NumberAM
NumberPM
toDays
toHours
toMinutes

DateAndConstraint  # Arguments: (1) :date1, the first date, (2) :date2, the second date. Returns: The date and constraint.
DateAtTimeWithDefaults  # Arguments: (1) :date, the date, (2) :time, the time. Returns: The date and time.
nextDayOfMonth  # Arguments: (1) the day of the month. Returns: The next occurrence of the day of the month.
DayOfWeek  # Arguments: (1) the day of the week. Returns: The day of the week.
DowOfWeekNew  # Arguments: (1) :dow, the day of the week, (2) :week, the week. Returns: The day of the week in the week.
previousDayOfWeek  # Arguments: (1) :dayOfWeek, the day of the week. Returns: The previous occurrence of the day of the week.
NextDOW  # Arguments: (1) :dow, the day of the week. Returns: The next occurrence of the day of the week.
EventAllDayStartingDateForPeriod  # Arguments: (1) :event, the event, (2) :period, the duration of the event, (3) :startDate, the start date of the event. Returns: The event with the specified start date and duration.
PeriodDuration  # Arguments: (1) :duration, the duration. Returns: The period duration.

MD  # Arguments: (1) :day, the day, (2) :month, the month. Returns: The date.
MDY  # Arguments: (1) :day, the day, (2) :month, the month, (3) :year, the year. Returns: The date.
Month  # Arguments: (1) the month. Returns: The month.
NextTime  # Arguments: (1) :time, the time. Returns: The next occurrence of the time.
HourMinuteAm  # Arguments: (1) :hours, the hours, (2) :minutes, the minutes. Returns: The time.
HourMinutePm  # Arguments: (1) :hours, the hours, (2) :minutes, the minutes. Returns: The time.
FullMonthofMonth  # Arguments: (1) :month, the month. Returns: The full month.

TimeAfterDateTime  # Arguments: (1) :dateTime, the date and time, (2) :time, the time after the date and time. Returns: The time after the date and time.
OnDateAfterTime  # Arguments: (1) :date, the date, (2) :time, the time after the date. Returns: The date after the time.
AroundDateTime  # Arguments: (1) :dateTime, the date and time. Returns: The time around the date and time.
```"""}
solution_prefix = ""
test_solution_prefix = ""
