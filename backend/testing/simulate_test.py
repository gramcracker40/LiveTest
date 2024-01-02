'''
handles setting up the simulation for 'tests' and 'submissions'
creates a test that is tied to a course (course_id must exist)
It then submits three different answer keys to this test. 

'''

import base64
import json                    
import requests
import os
from datetime import datetime

URL = 'http://localhost:8000'
TEST_URL = f'{URL}/test/'
SUBMISSION_URL = f'{URL}/submission/'
HEADERS = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

def create_test(name:str, image_path:str, num_questions:int, 
                course_id:int, start:datetime, end:datetime):
    '''
    image path: must be valid path to a png or jpg image to process. 
    '''
    try:
        # stringify the test key image that was passed using base64 and utf8
        with open(image_path, "rb") as f:
            im_bytes = f.read()   
        answer_key_str = base64.b64encode(im_bytes).decode("utf8")
        file_extension = os.path.splitext(image_path)[1][1:]
        print(f"FIle extension: {file_extension}")
        # build the json object and post the data to the API
        payload = json.dumps({"name": name, "answer_key": answer_key_str, "start_t": str(start), 
            "end_t":str(end), "num_questions": num_questions,
            "course_id": course_id, "file_extension": file_extension})
        response = requests.post(TEST_URL, data=payload, headers=HEADERS)
        data = response.json() 
        print(data)

        return data    
    except requests.exceptions.RequestException:
        print(response.text)


def create_submission(image_path:str, student_id:int, test_id:int):
    '''
    submits a answer sheet to a specific test id. 
    '''
    with open(image_path, "rb") as f:
        image = f.read()
    answer_key_str = base64.b64encode(image).decode("utf8")
    file_extension = os.path.splitext(image_path)[1][1:]

    if file_extension not in ['jpg', 'png']:
        return {"error": "the image of the answer sheet should be a .png or .jpg"}

    payload = json.dumps({"student_id": student_id, "answer_key": answer_key_str, 
                            "test_id": test_id, "file_extension": file_extension})
    response = requests.post(SUBMISSION_URL, data=payload, headers=HEADERS)

    if response.status_code == 200:
        print(f"Successfully submitted image: {image_path}\n\tstudent id: {student_id}\n\ttest_id: {test_id}\n")
        print(response.text)
    else:    
        print(f"Error: {response.status_code}, message: {response.text}")
    

if __name__ == "__main__":
    test_name = "Test One --Gg"
    start = datetime.strptime("2023-12-19 15:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime("2023-12-19 18:00:00", "%Y-%m-%d %H:%M:%S")
    num_questions = 45
    course_id = 1
    image_path = '../../real_examples/IMG_4161.jpg'

    submissions = [
        {
            "student_id": 1, 
            "image_path": image_path
        }, 
        {
            "student_id": 2, 
            "image_path": image_path
        }, 
        {
            "student_id": 3, 
            "image_path": image_path
        }
    ]
    new_test = create_test(test_name, image_path, 45, course_id, start, end)
    test_id = new_test['id']

    first_submission = create_submission(submissions[0]["image_path"], 
                submissions[0]["student_id"], test_id)
    second_submission = create_submission(submissions[1]["image_path"], 
                submissions[1]["student_id"], test_id)
    third_submission = create_submission(submissions[2]["image_path"], 
                submissions[2]["student_id"], test_id)
