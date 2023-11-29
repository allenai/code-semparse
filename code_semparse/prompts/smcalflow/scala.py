structures = {"full_dd": """```scala
case class Person(name: String) {
  def findTeamOf(): List[Person] = ???
  def findReportsOf(): List[Person] = ???
  def findManagerOf(): Person = ???
}

case class Event(var attendees: Option[List[Person]] = None,
                 var attendeesToAvoid: Option[List[Person]] = None,
                 var subject: Option[String] = None,
                 var location: Option[String] = None,
                 var startsAt: Option[List[DateTimeClause]] = None,
                 var endsAt: Option[List[DateTimeClause]] = None,
                 var duration: Option[TimeUnit] = None,
                 var showAsStatus: Option[ShowAsStatusType.Value] = None)

object DateTimeValues extends Enumeration {
  val Afternoon, Breakfast, Brunch, Dinner, Early, EndOfWorkDay, Evening,
  FullMonthofMonth, FullYearofYear, LastWeekNew, Late, LateAfternoon, LateMorning, Lunch, Morning,
  NextMonth, NextWeekend, NextWeekList, NextYear, Night, Noon, Now, SeasonFall, SeasonSpring,
  SeasonSummer, SeasonWinter, ThisWeek, ThisWeekend, Today, Tomorrow, Yesterday = Value
}

class DateTimeClause {
  def getByValue(dateTimeValue: DateTimeValues.Value): DateTimeClause = ???
  def getNextDow(dayOfWeek: String): DateTimeClause = ???
  def dateByMdy(month: Option[Int] = None, day: Option[Int] = None, year: Option[Int] = None): DateTimeClause = ???
  def timeByHm(hour: Option[Int] = None, minute: Option[Int] = None, amOrPm: Option[String] = None): DateTimeClause = ???
  def onDateBeforeDateTime(date: DateTimeClause, time: DateTimeClause): DateTimeClause = ???
  def onDateAfterDateTime(date: DateTimeClause, time: DateTimeClause): DateTimeClause = ???
  def aroundDateTime(dateTime: DateTimeClause): DateTimeClause = ???
}

object TimeUnits extends Enumeration {
  val Hours, Minutes, Days = Value
}

object TimeUnitsModifiers extends Enumeration {
  val Acouple, Afew = Value
}

case class TimeUnit(var number: Option[Either[Int, Double]] = None,
                    var unit: Option[TimeUnits.Value] = None,
                    var modifier: Option[TimeUnitsModifiers.Value] = None)

object ShowAsStatusType extends Enumeration {
  val Busy, OutOfOffice = Value
}

class API {
  def findPerson(name: String): Person = ???
  def getCurrentUser(): Person = ???
  def addEvent(event: Event): Unit = ???
  def findEvent(attendees: Option[List[Person]] = None, subject: Option[String] = None): Event = ???
}

val api = new API
```"""}

solution_prefix = ""
test_solution_prefix = ""
