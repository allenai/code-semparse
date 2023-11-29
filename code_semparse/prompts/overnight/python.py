structures = {"full_dd": """"
```python
Gender = Enum('Gender', 'male,female')
RelationshipStatus = Enum('RelationshipStatus', 'single,married')
Education = NamedTuple('Education', [('university', str), ('field_of_study', str), ('start_date', int), ('end_date', int)])
Employment = NamedTuple('Employment', [('employer', str), ('job_title', str), ('start_date', int), ('end_date', int)])

@dataclass
class Person:
    name: str
    gender: Gender
    relationship_status: RelationshipStatus
    height: int
    birthdate: int
    birthplace: str
    friends: List['Person'] = None
    logged_in: bool = False

    education: List[Education] = None
    employment: List[Employment] = None


@dataclass
class API:
    people: List[Block]
    
    def find_person_by_id(self, block_id: str) -> Person:
        ...

api = API()
```""", "no_typing": """"
```python
Gender = Enum('Gender', 'male,female')
RelationshipStatus = Enum('RelationshipStatus', 'single,married')
Education = NamedTuple('Education', [('university', str), ('field_of_study', str), ('start_date', int), ('end_date', int)])
Employment = NamedTuple('Employment', [('employer', str), ('job_title', str), ('start_date', int), ('end_date', int)])

@dataclass
class Person:
    name
    gender
    relationship_status
    height
    birthdate
    birthplace
    friends = None
    logged_in = False

    education = None
    employment = None


@dataclass
class API:
    people
    
    def find_person_by_id(self, block_id):
        ...

api = API()
```""", "list_of_operators": """"
```python
Gender
male
female
RelationshipStatus
single
married
Education
university
field_of_study
start_date
end_date
Employment
employer
job_title
start_date
end_date

Person
name
gender
relationship_status
height
birthdate
birthplace
friends
logged_in
education
employment

class API:
people
    
find_person_by_id
```"""}

solution_prefix = ""
test_solution_prefix = ""
