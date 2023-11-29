import json
import re

from dataclasses import dataclass
from typing import List

from tqdm import tqdm

from eval.overnight.dcs import execute_dcs


@dataclass
class Person:
    name: str
    gender: str
    relationship_status: str
    height: int
    birthdate: str
    birthplace: str
    friends: str
    logged_in: str

@dataclass
class Education:
    student: str
    university: str
    field_of_study: str
    education_start_date: str
    education_end_date: str

@dataclass
class Employment:
    employee: str
    employer: str
    job_title: str
    employment_start_date: str
    employment_end_date: str


@dataclass
class SocialNetworkDB:
    people: List[Person]
    education: List[Education]
    employment: List[Employment]

    @staticmethod
    def from_file(path: str):
        with open(path, "r") as f:
            db_contents = json.load(f)

        return SocialNetworkDB(
            people=[Person(**p) for p in db_contents["people"]],
            education=[Education(**e) for e in db_contents["education"]],
            employment=[Employment(**e) for e in db_contents["employment"]]
        )

    @staticmethod
    def from_java_api(save: bool = True):
        def get_entities(entity_type: str, domain: str):
            result_str = execute_dcs(f"(call SW.getProperty (call SW.singleton en.{entity_type}) (string !type))",
                                     domain)
            return re.findall(r"name ([^\)]*)", result_str)

        def get_entity_attr(entity_name: str, attr: str, domain: str):
            result_str = execute_dcs(f"(call SW.getProperty {entity_name} (string {attr}))", domain)
            return re.findall(r"\(list \(\w* ([^ ^\)]*)", result_str)[0]

        def get_entity_attr_with_other_entities(entity_name: str, attr: str, domain: str):
            result_str = execute_dcs(f"(call SW.getProperty {entity_name} (string {attr}))", domain)
            return re.findall(r"name ([^\)]*)", result_str)

        # there's probably a better way to do this, but this works in any case. We first get the names of all people,
        # then for each person we get all of its properties.
        all_people_names = get_entities("person", "socialnetwork")
        all_people = []
        for person_name in tqdm(all_people_names):
            person_attrs = {}
            for attr in ["gender", "relationship_status", "height", "birthdate", "birthplace"]:
                person_attrs[attr] = get_entity_attr(person_name, attr, "socialnetwork")

            try:
                person_attrs["friends"] = get_entity_attr_with_other_entities(person_name, "friend", "socialnetwork")
            except Exception as e:
                person_attrs["friends"] = []

            try:
                logged_in_str = get_entity_attr(person_name, "logged_in", "socialnetwork")
                person_attrs["logged_in"] = True
            except Exception as e:
                person_attrs["logged_in"] = False
            all_people.append(Person(**person_attrs, name=person_name))

        # get all education entries
        all_education_names = get_entities("education", "socialnetwork")
        all_education = []
        for education_name in tqdm(all_education_names):
            education_attrs = {}
            for attr in ["student", "university", "field_of_study", "education_start_date", "education_end_date"]:
                education_attrs[attr] = get_entity_attr(education_name, attr, "socialnetwork")
            all_education.append(Education(**education_attrs))

        # get all employment entries
        all_employment_names = get_entities("employment", "socialnetwork")
        all_employment = []
        for employment_name in tqdm(all_employment_names):
            employment_attrs = {}
            for attr in ["employee", "employer", "job_title", "employment_start_date", "employment_end_date"]:
                employment_attrs[attr] = get_entity_attr(employment_name, attr, "socialnetwork")
            all_employment.append(Employment(**employment_attrs))

        if save:
            with open("db_socialnetwork.json", "w") as f:
                db = {"people": [p.__dict__ for p in all_people], "education": [e.__dict__ for e in all_education], "employment": [e.__dict__ for e in all_employment]}
                json.dump(db, f)
        return SocialNetworkDB(all_people, all_education, all_employment)


if __name__ == '__main__':
    db = SocialNetworkDB.from_java_api(save=True)
    # db = peopleDB.from_file("db.json")
    print(db.people[0])
