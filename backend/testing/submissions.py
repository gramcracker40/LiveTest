import requests

url = "http://127.0.0.1:8000/submission/"

with open("40-6-const.png", "rb") as file:
    # Using the 'files' dictionary to send files and data
    files = {
        "submission_image": ("40-6-const.png", file, "image/png"),
        "student_id": (None, "1"),  # None indicates this is not a file but part of the data
        "test_id": (None, "1b73cfc1-b88a-4d98-bbcf-e1cbfb6afc9b"),
    }
    response = requests.post(url, files=files)

# Checking the response
if response.status_code == 200:
    print("Submission successful:", response.json())
else:
    print("Error submitting:", response.status_code, response.text)
