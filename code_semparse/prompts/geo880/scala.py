structures = {"full_dd": """"
```scala
case class State(name: String, abbreviation: String, country: Country, area: Int, size: Int, population: Int, density: Float, capital: Option[City], highPoint: Place, lowPoint: Place, nextTo: List[State], cities: List[City], places: List[Place], mountains: List[Mountain], lakes: List[Lake], rivers: List[River])

case class City(name: String, state: State, country: Country, isCapital: Boolean, population: Int, size: Int, isMajor: Boolean, density: Float)

case class Country(name: String, area: Int, population: Int, density: Float, highPoint: Place, lowPoint: Place, cities: List[City], states: List[State], places: List[Place], mountains: List[Mountain], lakes: List[Lake], rivers: List[River])

case class River(name: String, traverses: List[State], length: Int, size: Int, isMajor: Boolean)

case class Place(name: String, state: State, elevation: Int, size: Int)

case class Mountain(name: String, state: State, elevation: Int)

case class Lake(name: String, area: Int, states: List[State])

class GeoModel {
  var countries: List[Country] = List()
  var states: List[State] = List()
  var cities: List[City] = List()
  var rivers: List[River] = List()
  var mountains: List[Mountain] = List()
  var lakes: List[Lake] = List()
  var places: List[Place] = List()

  def findCountry(name: String): Option[Country] = ???

  def findState(name: String): Option[State] = ???

  def findCity(name: String, stateAbbreviation: Option[String] = None): Option[City] = ???

  def findRiver(name: String): Option[River] = ???

  def findMountain(name: String): Option[Mountain] = mountains.find(_.name == name)

  def findLake(name: String): Option[Lake] = lakes.find(_.name == name)

  def findPlace(name: String): Option[Place] = places.find(_.name == name)
}

val geoModel = new GeoModel()
```"""}

solution_prefix = "def answer() -> "
test_solution_prefix = ""
