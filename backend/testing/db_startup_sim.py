"""
populates the database with students, teachers, courses and enrollments
set the amounts below. It will handle the rest.

run this only with a blank database and the API running
because this runs off the assumption that the identifiers of the
objects created in db will be in ascending order from 1-100
"""
import json
import requests
from random import randint
from time import sleep

# API constants
URL = "http://localhost:8000"
COURSE_URL = f"{URL}/course/"
STUDENT_URL = f"{URL}/users/students/"
TEACHER_URL = f"{URL}/users/teachers/"
HEADERS = {"Content-Type": "application/json", "Accept": "text/plain"}

# constants for fake data creation
SEMESTER = "Fall"
SCHOOL_DOMAIN = "my.msutexas.edu"
NUM_STUDENTS = 1000
NUM_TEACHERS = 100
NUM_COURSES = 200
COURSES_PER_STUDENT = 5
subjects = ["MATH", "CMPS", "ENGL", "HIST", "CH"]
NUM_SUBJECTS = len(subjects)

# setup the fake resources used to populate the db
# generate the set number of fake students, teachers, and courses
students = [
    json.dumps(
        {
            "name": f"Student {i}",
            "email": f"student{i}@{SCHOOL_DOMAIN}",
            "password": "pass",
            "M_number": f"M20223{i}",
        }
    )
    for i in range(1, NUM_STUDENTS + 1)
]

teachers = [
    json.dumps(
        {
            "name": f"Teacher {i}",
            "email": f"teacher{i}@{SCHOOL_DOMAIN}",
            "password": "pass",
        }
    )
    for i in range(1, NUM_TEACHERS + 1)
]

courses = [
    json.dumps(
        {
            "name": f"Course {i}",
            "semester_season": SEMESTER,
            "course_number": randint(10000, 99999),
            "section": randint(1, 3),
            "year": 2023,
            "teacher_id": None,
            "subject": subjects[i % NUM_SUBJECTS],
        }
    )
    for i in range(1, NUM_COURSES + 1)
]

# create all of the students/teachers
for student in students:
    response = requests.post(STUDENT_URL, data=student, headers=HEADERS)

for teacher in teachers:
    response = requests.post(TEACHER_URL, data=teacher, headers=HEADERS)


# create the course and assign the teachers to a course based off %
for c_id, course in enumerate(courses):
    course_new_response = requests.post(COURSE_URL, data=course, headers=HEADERS)
    course_obj = json.loads(course)
    teacher_id = (c_id % NUM_TEACHERS) + 1
    
    course_update_teacher = requests.patch(
        f"{COURSE_URL}{c_id + 1}/",
        json={"teacher_id": teacher_id},
        headers=HEADERS,
    )
    print(f"added teacher {teacher_id} to course {c_id + 1}\n")

# create the enrollments of the students in the various courses at random. 
for s_id, student in enumerate(students):
    student_obj = json.loads(student)
    courses = []
    for each_enr in range(COURSES_PER_STUDENT):
        course_id = randint(1, NUM_COURSES)
        while course_id in courses:
            course_id = randint(1, NUM_COURSES)
        response = requests.post(
            f"{URL}/enrollment/{course_id}/student/{s_id + 1}", headers=HEADERS
        )
        courses.append(course_id)
        print(f"Added student {s_id + 1} to course {course_id}")
