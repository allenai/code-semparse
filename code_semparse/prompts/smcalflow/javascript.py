structures = {"full_dd": """```javascript
class Person {
    constructor(name) {
        this.name = name;
    }

    find_team_of() {
        // ...
    }

    find_reports_of() {
        // ...
    }

    find_manager_of() {
        // ...
    }
}

class Event {
    constructor(attendees = null, attendees_to_avoid = null, subject = null, location = null, starts_at = null, ends_at = null, duration = null, show_as_status = null) {
        this.attendees = attendees;
        this.attendees_to_avoid = attendees_to_avoid;
        this.subject = subject;
        this.location = location;
        this.starts_at = starts_at;
        this.ends_at = ends_at;
        this.duration = duration;
        this.show_as_status = show_as_status;
    }
}

const DateTimeValues = ["Afternoon", "Breakfast", "Brunch", "Dinner", "Early", "EndOfWorkDay", "Evening",
    "FullMonthofMonth", "FullYearofYear", "LastWeekNew", "Late", "LateAfternoon", "LateMorning", "Lunch", "Morning",
    "NextMonth", "NextWeekend", "NextWeekList", "NextYear", "Night", "Noon", "Now", "SeasonFall", "SeasonSpring",
    "SeasonSummer", "SeasonWinter", "ThisWeek", "ThisWeekend", "Today", "Tomorrow", "Yesterday"];

class DateTimeClause {
    get_by_value(date_time_value) {
        // ...
    }

    get_next_dow(day_of_week) {
        // ...
    }

    date_by_mdy(month = null, day = null, year = null) {
        // ...
    }

    time_by_hm(hour = null, minute = null, am_or_pm = null) {
        // ...
    }

    on_date_before_date_time(date, time) {
        // ...
    }

    on_date_after_date_time(date, time) {
        // ...
    }

    around_date_time(date_time) {
        // ...
    }
}

const TimeUnits = ["Hours", "Minutes", "Days"];
const TimeUnitsModifiers = ["Acouple", "Afew"];

class TimeUnit {
    constructor(number = null, unit = null, modifier = null) {
        this.number = number;
        this.unit = unit;
        this.modifier = modifier;
    }
}

const ShowAsStatusType = ["Busy", "OutOfOffice"];

class API {
    find_person(name) {
        // ...
    }

    get_current_user() {
        // ...
    }

    add_event(event) {
        // ...
    }

    find_event(attendees = null, subject = null) {
        // ...
    }
}

const api = new API();
```"""}

solution_prefix = ""
test_solution_prefix = ""
