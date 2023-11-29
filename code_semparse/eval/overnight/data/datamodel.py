from dataclasses import dataclass
from enum import Enum
from typing import List, NamedTuple

from eval.datamodel_helper import skip
from eval.overnight.data.database import SocialNetworkDB

Gender = Enum('Gender', 'male,female')
RelationshipStatus = Enum('RelationshipStatus', 'single,married')
Education = NamedTuple('Education', [('university', str), ('field_of_study', str), ('start_date', str), ('end_date', str)])
Employment = NamedTuple('Employment', [('employer', str), ('job_title', str), ('start_date', str), ('end_date', str)])

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

    def __repr__(self):
        return f"Person(name={self.name})"


@dataclass
class API:
    people: List[Person]

    _person_by_id = {}

    def find_person_by_id(self, person_id: str) -> Person:
        return next(filter(lambda person: person.name == person_id, self.people))

    @skip
    @staticmethod
    def from_file(path: str):
        person_by_id = {}

        db = SocialNetworkDB.from_file(path)
        for db_person in db.people:
            person_by_id[db_person.name] = Person(
                name=db_person.name,
                gender=Gender[db_person.gender.split(".")[-1]],
                relationship_status=RelationshipStatus[db_person.relationship_status.split(".")[-1]],
                height=int(db_person.height),
                birthdate=int(db_person.birthdate),
                birthplace=db_person.birthplace,
                logged_in=db_person.logged_in == "true",
                friends=[],
                education=[],
                employment=[]
            )

        for db_person in db.people:
            person_by_id[db_person.name].friends = [person_by_id[friend] for friend in db_person.friends]

        for db_education in db.education:
            person_by_id[db_education.student].education.append(Education(
                university=db_education.university,
                field_of_study=db_education.field_of_study,
                start_date=int(db_education.education_start_date),
                end_date=int(db_education.education_end_date)
            ))

        for db_employment in db.employment:
            person_by_id[db_employment.employee].employment.append(Employment(
                employer=db_employment.employer,
                job_title=db_employment.job_title,
                start_date=int(db_employment.employment_start_date),
                end_date=int(db_employment.employment_end_date)
            ))

        return API(list(person_by_id.values()))


if __name__ == "__main__":
    api = API.from_file("db_socialnetwork.json")


    # def answer():
    #     students_with_most_majors = []
    #     max_majors = max([len(set([education.field_of_study for education in student.education])) for student in api.people])
    #     for student in api.people:
    #         if len(set([education.field_of_study for education in student.education])) == max_majors:
    #             students_with_most_majors.append(student)
    #     return students_with_most_majors

    def answer():
        employees_with_few_employers = [person for person in api.people if 1 <= len(set([e.employer for e in person.employment])) <= 2]
        return employees_with_few_employers



    print(answer())