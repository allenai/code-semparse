structures = {
    "list_of_operators": """```
listValue
filter
getProperty
reverse
singleton
domain  domain
countSuperlative
ensureNumericProperty
ensureNumericEntity
size
aggregate
concat
countComparative
superlative

lambda
var
string
number
date

en.person
en.company
en.university
en.relationship_status
en.employee
en.student
en.field
en.city
en.gender

en.gender.female
en.gender.male
en.relationship_status
en.relationship_status.single
en.relationship_status.married

height
birthdate
birthplace
logged_in
friend
relationship_status

student
university
field_of_study
education_start_date
education_end_date

employee
employer
job_title
employment_start_date
employment_end_date
""", "full_dd": """```
listValue  # extract values from an object. Arguments: (1) An object of any type. Returns: A list of values.
filter  # applies a filter to a list of objects. Arguments: (1) A list of objects, (2) A property to filter on, (3) A comparison operator, (4) A value to compare against. If property is boolean (unary), arguments: (1) A list of objects, (2) Unary property to filter on. Returns: A list of objects that pass the filter.
getProperty  # retrieves a property from an object. Arguments: (1) An object, (2) A property name. Returns: The value of the property.
reverse  # reverses the direction of a property. Arguments: (1) A property name. Returns: The reversed property name.
singleton  # creates a singleton set containing a single object. Arguments: (1) An object. Returns: A singleton set containing the object.
domain  # retrieves the domain of a property, which is the set of entities or objects that the property can be applied to. Arguments: (1) A property name. Returns: The set of entities that can have the property.
countSuperlative  # finds the object(s) with the minimum or maximum count of a certain property. Arguments: (1) A list of objects, (2) A superlative operator (min or max), (3) A property to count, (4) A list of objects to count from. Returns: The object(s) with the minimum or maximum count of the property.
ensureNumericProperty  # ensures that a property is treated as numeric for comparison purposes. Arguments: (1) A property name. Returns: The property name, treated as numeric.
ensureNumericEntity  # ensures that an entity is treated as numeric for comparison purposes. Arguments: (1) An entity. Returns: The entity, treated as numeric.
size  # retrieves the size of a collection. Arguments: (1) A collection of objects. Returns: The size of the collection as a numeric value.
aggregate  # applies an aggregate function to a property over a set of objects. Arguments: (1) An aggregate function (e.g., sum, avg, min, max), (2) A property to aggregate over, (3) A set of objects. Returns: The result of the aggregate function.
concat  # concatenates two or more strings or lists. Arguments: (1 and subsequent) Strings or lists to concatenate. Returns: The concatenated result.
countComparative  # compares the count of a property over a set of objects with a given number. Arguments: (1) A set of objects, (2) A property to count, (3) A comparison operator, (4) A number to compare against, (5) A set of objects to count from. Returns: The objects for which the count of the property satisfies the comparison.
superlative  # finds the object(s) with the minimum or maximum value of a certain property. Arguments: (1) A set of objects, (2) A superlative operator (min or max), (3) A property to compare. Returns: The object(s) with the minimum or maximum value of the property.

lambda  # creates a function. Arguments: (1) A variable name, (2) A function body. Returns: A function.
var  # references a variable. Arguments: (1) A variable name. Returns: The value of the variable.

# The following are namespaces for different types of entities.
en.person
en.company
en.university
en.relationship_status
en.employee
en.student
en.field
en.city
en.gender

# specific entities under these namespaces:
en.gender.female
en.gender.male
en.relationship_status
en.relationship_status.single
en.relationship_status.married

# en.person properties:
height  # property of type (number with unit en.cm)
birthdate  # property of type date
birthplace  # property of type en.city
logged_in  # property of type bool
friend  # property of type en.person
relationship_status  # property of type en.relationship_status

# education properties:
student  # property of type en.person
university  # property of type en.university
field_of_study  # property of type en.field
education_start_date  # property of type date
education_end_date  # property of type date

# employment properties:
employee  # property of type en.person
employer  # property of type en.company
job_title  # property of type string
employment_start_date  # property of type date
employment_end_date  # property of type date
"""}

solution_prefix = ""
test_solution_prefix = ""

