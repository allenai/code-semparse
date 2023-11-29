structures = {"full_dd": """"
```javascript
class State {
    constructor(name, abbreviation, country, area, size, population, density, capital, high_point, low_point, next_to, cities, places, mountains, lakes, rivers) {
        this.name = name;
        this.abbreviation = abbreviation;
        this.country = country;
        this.area = area;
        this.size = size;
        this.population = population;
        this.density = density;
        this.capital = capital;
        this.high_point = high_point;
        this.low_point = low_point;
        this.next_to = next_to;
        this.cities = cities;
        this.places = places;
        this.mountains = mountains;
        this.lakes = lakes;
        this.rivers = rivers;
    }
}

class City {
    constructor(name, state, country, is_capital, population, size, is_major, density) {
        this.name = name;
        this.state = state;
        this.country = country;
        this.is_capital = is_capital;
        this.population = population;
        this.size = size;
        this.is_major = is_major;
        this.density = density;
    }
}

class Country {
    constructor(name, area, population, density, high_point, low_point, cities, states, places, mountains, lakes, rivers) {
        this.name = name;
        this.area = area;
        this.population = population;
        this.density = density;
        this.high_point = high_point;
        this.low_point = low_point;
        this.cities = cities;
        this.states = states;
        this.places = places;
        this.mountains = mountains;
        this.lakes = lakes;
        this.rivers = rivers;
    }
}

class River {
    constructor(name, traverses, length, size, is_major) {
        this.name = name;
        this.traverses = traverses;
        this.length = length;
        this.size = size;
        this.is_major = is_major;
    }
}

class Place {
    constructor(name, state, elevation, size) {
        this.name = name;
        this.state = state;
        this.elevation = elevation;
        this.size = size;
    }
}

class Mountain {
    constructor(name, state, elevation) {
        this.name = name;
        this.state = state;
        this.elevation = elevation;
    }
}

class Lake {
    constructor(name, area, states) {
        this.name = name;
        this.area = area;
        this.states = states;
    }
}

class GeoModel {
    constructor(countries, states, cities, rivers, mountains, lakes, places) {
        this.countries = countries;
        this.states = states;
        this.cities = cities;
        this.rivers = rivers;
        this.mountains = mountains;
        this.lakes = lakes;
        this.places = places;
    }

    find_country(name) {
        // ...
    }

    find_state(name) {
        // ...
    }

    find_city(name, state_abbreviation = null) {
        // ...
    }

    find_river(name) {
        // ...
    }

    find_mountain(name) {
        // ...
    }

    find_lake(name) {
        // ...
    }

    find_place(name) {
        // ...
    }
}

let geo_model = new GeoModel();
```"""}

solution_prefix = ""
test_solution_prefix = ""
