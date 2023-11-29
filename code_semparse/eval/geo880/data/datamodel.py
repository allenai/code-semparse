from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional, List

from eval.geo880.data.database import GeoDB


def _remove_duplicates(list_of_objects: List, key="name") -> List:
    seen = set()
    new_list = []
    for obj in list_of_objects:
        if getattr(obj, key) not in seen:
            new_list.append(obj)
            seen.add(getattr(obj, key))
    return new_list


@dataclass
class State:
    name: str = None
    abbreviation: str = None
    country: Country = None
    area: int = None
    population: int = None
    capital: Optional[City] = None
    high_point: Place = None
    low_point: Place = None
    next_to: List[State] = field(default_factory=lambda: [])
    cities: List[City] = field(default_factory=lambda: [])
    places: List[Place] = field(default_factory=lambda: [])
    mountains: List[Mountain] = field(default_factory=lambda: [])
    lakes: List[Lake] = field(default_factory=lambda: [])
    rivers: List[River] = field(default_factory=lambda: [])

    @property
    def size(self) -> int:
        return self.area

    @property
    def density(self) -> float:
        return self.population / self.area

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

@dataclass
class City:
    name: str = None
    state: State = None
    country: Country = None
    is_capital: bool = None
    population: int = None

    @property
    def is_major(self) -> bool:
        return self.population > 150000

    @property
    def size(self) -> int:
        return self.population

    @property
    def density(self) -> float:
        # density isn't defined for cities since there's no area, but this is still used in geoquery
        return 1

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name), hash(self.state)

@dataclass
class Country:
    name: str = None
    population: int = None
    area: int = None
    high_point: Place = None
    low_point: Place = None
    cities: List[City] = field(default_factory=lambda: [])
    states: List[State] = field(default_factory=lambda: [])
    places: List[Place] = field(default_factory=lambda: [])
    mountains: List[Mountain] = field(default_factory=lambda: [])
    lakes: List[Lake] = field(default_factory=lambda: [])
    rivers: List[River] = field(default_factory=lambda: [])

    @property
    def density(self) -> float:
        return self.population / self.area

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

@dataclass
class River:
    name: str = None
    traverses: List[State] = None
    length: int = None

    @property
    def size(self) -> int:
        return self.length

    @property
    def is_major(self) -> bool:
        return self.length > 750

    def __repr__(self):
        return self.name

@dataclass
class Place:
    name: str = None
    state: State = None
    elevation: int = None

    @property
    def size(self) -> int:
        return self.elevation

    def __repr__(self):
        return self.name

@dataclass
class Mountain:
    name: str = None
    state: State = None
    elevation: int = None

    def __repr__(self):
        return self.name

@dataclass
class Lake:
    name: str = None
    area: int = None
    states: List[State] = field(default_factory=lambda: [])

    def __repr__(self):
        return self.name


def longer(river_1: River, river_2: River) -> bool:
    return river_1.length > river_2.length


def higher(place_1: Place, place_2: Place) -> bool:
    return place_1.elevation > place_2.elevation


def lower(place_1: Place, place_2: Place) -> bool:
    return place_1.elevation < place_2.elevation


@dataclass
class GeoModel:
    states: List[State]
    cities: List[City]
    rivers: List[River]
    mountains: List[Mountain]
    lakes: List[Lake]
    places: List[Place]
    countries: List[Country]

    def find_country(self, name: str) -> Country:
        return self.countries[0]

    def find_state(self, name: str) -> State:
        return next((s for s in self.states if s.name == name.lower()), None)

    def find_city(self, name: str, state_abbreviation: str = None) -> City:
        if state_abbreviation:
            return next((c for c in self.cities if c.name == name.lower() and c.state.abbreviation == state_abbreviation.lower()), None)
        else:
            return next((c for c in self.cities if c.name == name.lower()), None)

    def find_river(self, name: str) -> River:
        return next((r for r in self.rivers if r.name == name.lower()), None)

    def find_mountain(self, name: str) -> Mountain:
        return next((m for m in self.mountains if m.name == name.lower()), None)

    def find_lake(self, name: str) -> Lake:
        return next((l for l in self.lakes if l.name == name.lower()), None)

    def find_place(self, name: str) -> Place:
        return next((p for p in self.places if p.name == name.lower()), None)

    @classmethod
    def from_db(cls, geodb: GeoDB):
        partial_states = defaultdict(State)
        partial_cities = defaultdict(City)
        partial_rivers = defaultdict(River)
        partial_mountains = defaultdict(Mountain)
        partial_lakes = defaultdict(Lake)
        partial_places = defaultdict(Place)
        country = Country(
            name='usa',
            population=geodb.countries[0].population,
            area=geodb.countries[0].area,
        )

        for s in geodb.states:
            partial_states[s.name] = State(
                name=s.name,
                abbreviation=s.abbreviation,
                country=country,
                area=s.area,
                population=s.population
            )

        for c in geodb.cities:
            state = partial_states[c.state]
            city = City(
                name=c.name,
                state=state,
                country=country,
                population=c.population,
                is_capital=c.name == [s for s in geodb.states if s.name == c.state][0].capital
            )
            if city.is_capital:
                state.capital = city
            if c.name not in [sc.name for sc in partial_states[c.state].cities]:
                partial_states[c.state].cities.append(city)
            partial_cities[(c.name, c.state)] = city

        for s in geodb.states:
            if not partial_states[s.name].capital:
                # city isn't under "cities" list, so we need to create it
                city = City(
                    name=s.capital,
                    state=partial_states[s.name],
                    country=country,
                    is_capital=True
                )
                partial_states[s.name].capital = city

        for b in geodb.borders:
            partial_states[b.state].next_to = [partial_states[s] for s in b.states]

        for r in geodb.rivers:
            river = River(
                name=r.name,
                length=r.length,
                traverses=_remove_duplicates([partial_states[s] for s in r.traverses]),
            )
            partial_rivers[r.name] = river
            for s in r.traverses:
                if r.name not in [r.name for r in partial_states[s].rivers]:
                    partial_states[s].rivers.append(river)

        for m in geodb.mountains:
            mountain = Mountain(
                name=m.name,
                state=partial_states[m.state],
                elevation=m.height,
            )
            partial_mountains[m.name] = mountain
            partial_states[m.state].mountains.append(mountain)

        for l in geodb.lakes:
            lake = Lake(
                name=l.name,
                states=[partial_states[s] for s in l.states],
                area=l.area,
            )
            partial_lakes[l.name] = lake
            for state in lake.states:
                state.lakes.append(lake)
        
        for hl in geodb.highlows:
            highest_place = Place(
                name=hl.highest_point,
                state=partial_states[hl.state],
                elevation=hl.highest_elevation
            )
            lowest_place = Place(
                name=hl.lowest_point,
                state=partial_states[hl.state],
                elevation=hl.lowest_elevation
            )
            ps = partial_states[hl.state]
            ps.high_point = highest_place
            ps.low_point = lowest_place
            ps.places.extend([highest_place, lowest_place])
            partial_places[hl.highest_point] = highest_place
            partial_places[hl.lowest_point] = lowest_place

        c = geodb.countries[0]
        assert c.name == 'usa'
        country.states = list(partial_states.values())
        country.cities = list(partial_cities.values())
        country.rivers = list(partial_rivers.values())
        country.mountains = list(partial_mountains.values())
        country.lakes = list(partial_lakes.values())
        country.places = list(partial_places.values())
        return cls(
            countries=[country],
            states=list(partial_states.values()),
            cities=list(partial_cities.values()),
            rivers=list(partial_rivers.values()),
            mountains=list(partial_mountains.values()),
            lakes=list(partial_lakes.values()),
            places=list(partial_places.values()),
        )

def max_ignore_nans(*args, **kwargs):
    # geoquery database is inconsistent since it defines capitals with no corresponding cities, which results in None values for sizes,
    # so just like in the prolog version, we will ignore such cases
    if len(args) == 1 and type(args[0]) is list:
        args = args[0]

    # keep only non-Nones
    if "key" in kwargs:
        args = [arg for arg in args if kwargs["key"](arg) is not None]
    else:
        args = [arg for arg in args if arg is not None]

    # Call built-in function max with preprocessed args
    try:
        return max(args, **kwargs)
    except ValueError: # If all arguments were None
        return None

def min_ignore_nans(*args, **kwargs):
    # geoquery database is inconsistent since it defines capitals with no corresponding cities, which results in None values for sizes,
    # so just like in the prolog version, we will ignore such cases
    if len(args) == 1 and type(args[0]) is list:
        args = args[0]

    # keep only non-Nones
    if "key" in kwargs:
        args = [arg for arg in args if kwargs["key"](arg) is not None]
    else:
        args = [arg for arg in args if arg is not None]

    # Call built-in function max with preprocessed args
    try:
        return min(args, **kwargs)
    except ValueError: # If all arguments were None
        return None


if __name__ == '__main__':
    filepath = 'eval/geo880/data/geobase'
    geodb = GeoDB.from_db_file(filepath)
    geo_model = GeoModel.from_db(geodb)

    max_ignore_nans(1,3,2)

    mount_mckinley = geo_model.find_mountain('mount mckinley')
    print(mount_mckinley.elevation)
