structures = {"full_dd": """
```python
@dataclass
class State:
    name: str
    abbreviation: str
    country: Country
    area: int
    size: int
    population: int
    density: float
    capital: Optional[City]
    high_point: Place
    low_point: Place
    next_to: List[State]
    cities: List[City]
    places: List[Place]
    mountains: List[Mountain]
    lakes: List[Lake]
    rivers: List[River]

@dataclass
class City:
    name: str
    state: State
    country: Country
    is_capital: bool
    population: int
    size: int
    is_major: bool
    density: float

@dataclass
class Country:
    name: str
    area: int
    population: int
    density: float
    high_point: Place
    low_point: Place
    cities: List[City]
    states: List[State]
    places: List[Place]
    mountains: List[Mountain]
    lakes: List[Lake]
    rivers: List[River]

@dataclass
class River:
    name: str
    traverses: List[State]
    length: int
    size: int
    is_major: bool

@dataclass
class Place:
    name: str
    state: State
    elevation: int
    size: int

@dataclass
class Mountain:
    name: str
    state: State
    elevation: int

@dataclass
class Lake:
    name: str
    area: int
    states: List[State]

@dataclass
class GeoModel:
    countries: List[Country]
    states: List[State]
    cities: List[City]
    rivers: List[River]
    mountains: List[Mountain]
    lakes: List[Lake]
    places: List[Place]

    def find_country(self, name: str) -> Country:
        ...

    def find_state(self, name: str) -> State:
        ...

    def find_city(self, name: str, state_abbreviation: str = None) -> City:
        ...

    def find_river(self, name: str) -> River:
        ...

    def find_mountain(self, name: str) -> Mountain:
        ...

    def find_lake(self, name: str) -> Lake:
        ...

    def find_place(self, name: str) -> Place:
        ...

geo_model = GeoModel()
```""".strip(), "no_typing": """
```python
@dataclass
class State:
    name
    abbreviation
    country
    area
    population
    density
    capital
    high_point
    low_point
    next_to
    cities
    places
    mountains
    lakes
    rivers

@dataclass
class City:
    name
    state
    country
    is_capital
    population
    size
    is_major

@dataclass
class Country:
    name

@dataclass
class River:
    name
    traverses
    length
    size
    is_major

@dataclass
class Place:
    name
    state
    elevation
    size

@dataclass
class Mountain:
    name
    state
    elevation

@dataclass
class Lake:
    name
    area
    states

@dataclass
class GeoModel:
    countries
    states
    cities
    rivers
    mountains
    lakes
    places

    def find_country(self, name):
        ...

    def find_state(self, name):
        ...

    def find_city(self, name, state_abbreviation = None):
        ...

    def find_river(self, name):
        ...

    def find_mountain(self, name):
        ...

    def find_lake(self, name):
        ...

    def find_place(self, name):
        ...

geo_model = GeoModel()
```""".strip(), "list_of_operators": """
```python
State
name
abbreviation
country
area
population
density
capital
high_point
low_point
next_to
cities
places
mountains
lakes
rivers

City
name
state
country
is_capital
population
size
is_major

Country
name

River
name
traverses
length
size
is_major

Place
name
state
elevation
size

Mountain
name
state
elevation

Lake
name
area
states

GeoModel
countries
states
cities
rivers
mountains
lakes
places

find_country
find_state
find_city
find_river
find_mountain
find_lake
find_place
```""".strip()}

solution_prefix = "def answer() -> "
test_solution_prefix = ""
