import re
import ast
import attr
from attr import field
from dataclasses import dataclass

@attr.s(auto_attribs=True)
class state:
    name: str
    abbreviation: str
    capital: str
    population: float
    area: float
    state_number: int
    city1: str
    city2: str
    city3: str
    city4: str

@attr.s(auto_attribs=True)
class city:
    state: str
    stateid: str
    name: str
    population: int

@attr.s(auto_attribs=True)
class river:
    name: str
    length: float
    traverses: list[str]

@attr.s(auto_attribs=True)
class border:
    state: str
    stateid: str
    states: list[str]

@attr.s(auto_attribs=True)
class highlow:
    state: str
    stateid: str
    highest_point: str
    highest_elevation: float
    lowest_point: str
    lowest_elevation: float

@attr.s(auto_attribs=True)
class mountain:
    state: str
    stateid: str
    name: str
    height: float

@attr.s(auto_attribs=True)
class road:
    number: int
    states: list[str]

@attr.s(auto_attribs=True)
class lake:
    name: str
    area: int
    states: list[str]

@attr.s(auto_attribs=True)
class Country:
    name: str
    population: int
    area: int

@attr.s(auto_attribs=True)
class GeoDB:
    states: list[state]
    cities: list[city]
    rivers: list[river]
    borders: list[border]
    highlows: list[highlow]
    mountains: list[mountain]
    roads: list[road]
    lakes: list[lake]
    countries: list[Country]

    @classmethod
    def from_db_file(cls, filepath):
        db = dict(
            state=(state, []),
            city=(city, []),
            river=(river, []),
            border=(border, []),
            highlow=(highlow, []),
            mountain=(mountain, []),
            road=(road, []),
            lake=(lake, []),
            country=(Country, []),
        )

        for l in open(filepath).readlines()[22:]:
            key = l[:l.find('(')]
            try:
                parse = ast.literal_eval(l[len(key):-2])
                db[key][1].append(db[key][0](*parse))
            except:
                print(l)
        return cls(*[v[1] for v in db.values()])

if __name__ == '__main__':
    filepath = 'data/geoquery/geobase'
    geodb = GeoDB.from_db_file(filepath)
