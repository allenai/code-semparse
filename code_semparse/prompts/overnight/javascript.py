structures = {"full_dd": """"
```javascript
const Gender = Object.freeze({"male":1, "female":2});
const RelationshipStatus = Object.freeze({"single":1, "married":2});

class Education {
    constructor(university, field_of_study, start_date, end_date) {
        this.university = university;
        this.field_of_study = field_of_study;
        this.start_date = start_date;
        this.end_date = end_date;
    }
}

class Employment {
    constructor(employer, job_title, start_date, end_date) {
        this.employer = employer;
        this.job_title = job_title;
        this.start_date = start_date;
        this.end_date = end_date;
    }
}

class Person {
    constructor(name, gender, relationship_status, height, birthdate, birthplace, friends = [], logged_in = false, education = [], employment = []) {
        this.name = name;
        this.gender = gender;
        this.relationship_status = relationship_status;
        this.height = height;
        this.birthdate = birthdate;
        this.birthplace = birthplace;
        this.friends = friends;
        this.logged_in = logged_in;
        this.education = education;
        this.employment = employment;
    }
}

class API {
    constructor(people = []) {
        this.people = people;
    }

    find_person_by_id(block_id) { ... }
}

let api = new API();
```"""}

solution_prefix = ""
test_solution_prefix = ""
