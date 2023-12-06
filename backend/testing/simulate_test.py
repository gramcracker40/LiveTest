import base64
import json                    
import requests
import os
from datetime import datetime

url = 'http://localhost:8000/test/'
headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

def create_test(image_path:str, num_questions:int, 
                course_id:int, start:datetime, end:datetime):
    '''
    image path: must be valid path to a png or jpg image to process. 
    '''
    try:
        # stringify the test key image that was passes using base64 and utf8
        with open(image_path, "rb") as f:
            im_bytes = f.read()     
        answer_key_str = base64.b64encode(im_bytes).decode("utf8")

        # build the json object and post the data to the API
        payload = json.dumps({"answer_key": answer_key_str, "start_t": str(start), 
                            "end_t":str(end), "num_questions": num_questions,
                            "course_id": course_id})
        response = requests.post(url, data=payload, headers=headers)
        data = response.json()     
        print(data)
    except requests.exceptions.RequestException:
        print(response.text)


start = datetime.strptime("2023-12-06 15:30:00", "%Y-%m-%d %H:%M:%S")
end = datetime.strptime("2023-12-06 17:00:00", "%Y-%m-%d %H:%M:%S")
num_questions = 45
course_id = 1
image_path = '../../real_examples/IMG_4161.jpg'

new_test = create_test(image_path, 45, )