structures = {"full_dd": """"
```scala
object Gender extends Enumeration {
  type Gender = Value
  val Male, Female = Value
}

object RelationshipStatus extends Enumeration {
  type RelationshipStatus = Value
  val Single, Married = Value
}

case class Education(university: String, fieldOfStudy: String, startDate: LocalDate, endDate: LocalDate)
case class Employment(employer: String, jobTitle: String, startDate: LocalDate, endDate: LocalDate)

case class Person(
  name: String,
  gender: Gender.Gender,
  relationshipStatus: RelationshipStatus.RelationshipStatus,
  height: Int,
  birthdate: LocalDate,
  birthplace: String,
  friends: Option[List[Person]] = None,
  loggedIn: Boolean = false,
  education: Option[List[Education]] = None,
  employment: Option[List[Employment]] = None
)

class API {
  var people: List[Person] = List()

  def findPersonById(personId: String): Person = ???
}

val api = new API
```"""}

solution_prefix = ""
test_solution_prefix = ""
