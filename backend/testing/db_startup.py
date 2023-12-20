import json                    
import requests
import os
from datetime import datetime

URL = 'http://localhost:8000/users'
STUDENT_URL = f'{URL}/students'
TEACHER_URL = f'{URL}/teachers'
HEADERS = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

students = [{
    "name": f"Student {i}",
    "email": f"student{i}@example.com",
    "password": "pass",
    "M_number": f"M20223{i}"
    } for i in range(1, 101)]

teachers = [{
    "name": f"Teacher {i}",
    "email": f"teacher{i}@school.com",
    "password": "pass"
    } for i in range(1, 11)]

courses = []


