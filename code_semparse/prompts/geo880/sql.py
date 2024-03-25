structures = {
    "schema": """```
Table Name, Field Name, Is Primary Key, Is Foreign Key, Type
STATE, STATE_NAME, y, n, varchar(255)
STATE, CAPITAL, n, y, varchar(255)
STATE, POPULATION, n, n, int(11)
STATE, AREA, n, n, double
STATE, COUNTRY_NAME, n, n, varchar(255)
STATE, DENSITY, n, n, double
-, -, -, -, -
BORDER_INFO, STATE_NAME, y, y, varchar(255)
BORDER_INFO, BORDER, y, y, varchar(255)
-, -, -, -, -
CITY, CITY_NAME, y, n, varchar(255)
CITY, STATE_NAME, y, y, varchar(255)
CITY, POPULATION, n, n, int(11)
CITY, COUNTRY_NAME, n, n, varchar(255)
-, -, -, -, -
HIGHLOW, STATE_NAME, y, y, varchar(255)
HIGHLOW, HIGHEST_POINT, n, n, varchar(255)
HIGHLOW, HIGHEST_ELEVATION, n, n, varchar(255)
HIGHLOW, LOWEST_POINT, n, n, varchar(255)
HIGHLOW, LOWEST_ELEVATION, n, n, varchar(255)
-, -, -, -, -
RIVER, RIVER_NAME, y, n, varchar(255)
RIVER, LENGTH, n, n, int(11)
RIVER, TRAVERSE, y, y, varchar(255)
RIVER, COUNTRY_NAME, n, n, varchar(255)
-, -, -, -, -
MOUNTAIN, MOUNTAIN_NAME, y, n, varchar(255)
MOUNTAIN, MOUNTAIN_ALTITUDE, n, n, int(11)
MOUNTAIN, STATE_NAME, y, y, varchar(255)
MOUNTAIN, COUNTRY_NAME, n, n, varchar(255)
-, -, -, -, -
ROAD, ROAD_NAME, y, n, varchar(10)
ROAD, STATE_NAME, y, y, varchar(255)
-, -, -, -, -
LAKE, LAKE_NAME, y, n, varchar(255)
LAKE, AREA, n, n, double
LAKE, STATE_NAME, y, y, varchar(255)
LAKE, COUNTRY_NAME, n, n, varchar(255)
```""",
    }

solution_prefix = ""
test_solution_prefix = ""
