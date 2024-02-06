'''
built as the second step in the Scantron grading system
runs after the document has been isolates using isolate_document.py
'''


def crop_to_answers(image, left=0.145, right=0.58, top=0.155, bottom=0.94):
    """
    crop a Matlike image (cv2) given a left, right, top, bottom bound
    default: crops to scantrons answers
    """
    height, width = image.shape[:2]
    cropped = image.copy()

    left_bound = int(left * width)
    right_bound = int(right * width)

    top_bound = int(top * height)
    bottom_bound = int(bottom * height)

    return cropped[top_bound:bottom_bound, left_bound:right_bound]


def find_answer_numbers(image):
    '''
    find the answers 1-50
    '''
