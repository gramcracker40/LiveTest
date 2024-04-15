import requests
import os
from pathlib import Path
from answer_sheets.find_perfect import find_best_config
from answer_sheets.main import Pictron

DIRECTORY_PATH = '../answer_sheets/generatedSheets'  # Path to the directory containing images
API_URL = 'http://localhost:8000/submission/'  # URL to the FastAPI endpoint
TEST_ID = '1b73cfc1-b88a-4d98-bbcf-e1cbfb6afc9b'  # Example test ID, change as needed
TEST_NAME = 'Test #5 example'
COURSE_NAME = 'HIGHLY COMPLEX ALGEBRA V'
STUDENT_ID_START = 1
STUDENT_ID_END = 1


def student_id_generator(start, end):
    """Generate student IDs in a cycle from start to end."""
    while True:
        for id in range(start, end + 1):
            yield id

def create_submissions(test_id, num_questions, num_choices, student_id_start, student_id_end):
    student_ids = student_id_generator(student_id_start, student_id_end)
    current_student_id = next(student_ids) 

    answer_sheet_config = find_best_config(num_questions, num_choices)
    generator = Pictron(**answer_sheet_config)
    generator.generate(random_filled=True)


    files = {'submission_image': generator.image}
    data = {'student_id': current_student_id, 'test_id': test_id}
    
    response = requests.post(API_URL, files=files, data=data)
    print(f"Response from server for {current_student_id}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    create_submissions(DIRECTORY_PATH,  STUDENT_ID_START, STUDENT_ID_END, TEST_ID)

