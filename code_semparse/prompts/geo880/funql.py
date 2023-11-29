structures = {
    "full_dd": """```
cityid(CityName,StateAbbrev)  # given a city name and state, return the city id
countryid(CountryName)  # given a country name, return the country id
placeid(PlaceName)  # given a place (lakes, mountains, etc.) name, return the place id
riverid(RiverName)  # given a river name, return the river id
stateid(StateName)  # given a state name, return the state id

capital(all)  # return all cities that are capitals
city(all)  # return all cities
lake(all)  # return all lakes
mountain(all)  # return all mountains
place(all)  # return all places
river(all)  # return all rivers
state(all)  # return all states

capital(items)  # given a set of cities, return those that are capitals 
city(p)  # given a set of items, return those that are cities
lake(p)  # given a set of items, return those that are lakes
major(p)  # given a set of items, return those that are considered of major size
mountain(p)  # given a set of items, return those that are mountains
place(p)  # given a set of items, return those that are places
river(p)  # given a set of items, return those that are rivers
state(p)  # given a set of items, return those that are states
area_1(p)  # given a set of items, return their areas' sizes
capital_1(p)  # given a set of states, return their capitals
capital_2(p)  # given a set of cities, return their states
elevation_1(p)  # given a set of places, return their elevations
elevation_2(E)  # given a set of elevations, return the places with those elevations
high_point_1(p)  # given a set of items, return their highest points
high_point_2(p)  # given a set of places, return the items with those places as their highest points
higher_2(p)  # given a set of places, return the places that are higher than them
loc_1(p)  #  given a set of items, return where each item is located 
loc_2(p)  #  given a set of items, return the items located there
longer(p)  # given a set of rivers, return those that are longer than them
lower_2(p)  # given a set of places, return the places that are lower than them
len(p)  # given a set of rivers, return their lengths
next_to_1(p)  # given a set of states, return the states that are next to them
next_to_2(p)  # given a set of states, return the states that this state is next to
population_1(p)  # given a set of cities or states, return their populations
size(p)  # given a set of items, return their sizes (area for state, population for city, length for river)
traverse_1(p)  # given a set of rivers, return the states they traverse
traverse_2(p)  # given a set of states, return the rivers that traverse them

answer(p)  # return as answer (always needed)
largest(p)  # given a set of items, return the item with the largest size
largest_one(area_1(p))  # given a set of items, return the item with the largest area
largest_one(density_1(p))  # given a set of items, return the item with the largest density
largest_one(population_1(p))  # given a set of items, return the item with the largest population
smallest(p)  # given a set of items, return the item with the smallest size
smallest_one(area_1(p))  # given a set of items, return the item with the smallest area
smallest_one(density_1(p))  # given a set of items, return the item with the smallest density
smallest_one(population_1(p))  # given a set of items, return the item with the smallest population
highest(p)  # given a set of items, return the item that is highest
lowest(p)  # given a set of items, return the item that is lowest
longest(p)  # given a set of items, return the item that is longest
shortest(p)  # given a set of items, return the item that is shortest
count(p)  # given a set of items, return the number of items in the set
most(pD)  # given a set of items, return the item that appears most frequently in the set
fewest(pD)  # given a set of items, return the item that appears fewest times in the set

exclude(p1, p2)  # given a set of items, return the items that are in p1 but not in p2
intersect(p1, p2)  # given a set of items, return the items that are in both p1 and p2
```""",
    "list_of_operators": """```
cityid
countryid
placeid
riverid
stateid

capital
city
lake
mountain
place
river
state

capital
city
lake
major
mountain
place
river
state
area_1
capital_1
capital_2
elevation_1
elevation_2
high_point_1
high_point_2
higher_2
loc_1
loc_2
longer
lower_2
len
next_to_1
next_to_2
population_1
size
traverse_1
traverse_2

answer(p)
largest(p)
largest_one(area_1(p))
largest_one(density_1(p))
largest_one(population_1(p))
smallest(p)
smallest_one(area_1(p))
smallest_one(density_1(p))
smallest_one(population_1(p))
highest(p)
lowest(p)
longest(p)
shortest(p)
count(p)
most(pD)
fewest(pD)

exclude(p1, p2)
intersect(p1, p2)
```""",
    "formal": """```
def cityid(CityName: str, StateAbbrev: str) -> City: ...
def countryid(CountryName: str) -> Country: ...
def placeid(PlaceName: str) -> Place: ...
def riverid(RiverName: str) -> River: ...
def stateid(StateName: str) -> State: ...
def capital(places: List[Place]) -> List[City]: ...
def city(places: List[Place]) -> List[City]: ...
def lake(places: List[Place]) -> List[Lake]: ...
def mountain(places: List[Place]) -> List[Mountain]: ...
def place(places: List[Place]) -> List[Place]: ...
def river(places: List[Place]) -> List[River]: ...
def state(places: List[Place]) -> List[State]: ...
def major(places: List[Place]) -> List[Place]: ...
def area_1(state: State | List[State]) -> List[float]: ...
def capital_1(state: State | List[State]) -> List[City]: ...
def capital_2(city: City | List[City]) -> List[State]: ...
def density_1(state: State | List[State]) -> List[float]: ...
def elevation_1(place: List[Place]) -> List[floats]: ...
def elevation_2(elevation: float) -> List[Place]: ...
def high_point_1(state: State | List[State]) -> List[Place]: ...
def high_point_2(place: Place) -> List[State]: ...
def higher_2(place: Place) -> List[Place]: ...
def loc_1(place: Place | List[Place]) -> List[State]: ...
def loc_2(state: State | List[State]) -> List[Place]: ...
def longer(river: River) -> List[River]: ...
def lower_2(place: Place) -> List[Place]: ...
def len(river: River | List[River]) -> List[float]: ...
def next_to_1(state: State | List[State]) -> List[State]: ...
def next_to_2(state: State | List[State]) -> List[State]: ...
def population_1(state: State | List[State]) -> List[float]: ...
def size(place: List[State] | List[City]) -> List[float]: ...
def traverse_1(river: River | List[River]) -> List[State]: ...
def traverse_2(state: State | List[State] | Country | List[Country]) -> List[River]: ...
def largest(place: List[Place]) -> List[Place]: ...
def largest_one(lst: List[Place]) -> Place: ...
def smallest(place: List[Place]) -> List[Place]: ...
def smallest_one(lst: List[Place]) -> Place: ...

def highest(place: List[Place]) -> List[Place]: ...
def lowest(place: List[Place]) -> List[Place]: ...
def longest(place: List[Place]) -> List[River]: ...
def shortest(place: List[Place]) -> List[River]: ...
def count(place: List[Place]) -> List[int]: ...
def most(place: List[Place]) -> Place: ...
def fewest(place: List[Place]) -> Place: ...

def exclude(lst1: List[Place], lst2: List[Place]) -> List[Place]: ...
def intersect(lst1: List[Place], lst2: List[Place]) -> List[Place]: ...
```"""
    }

solution_prefix = ""
test_solution_prefix = ""
