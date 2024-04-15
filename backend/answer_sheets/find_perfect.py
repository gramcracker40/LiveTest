'''
Purpose: to find the best templated configuration possible for the 
given number of questions and choices in usage with Pictron. 
'''
# from main import Pictron
from answer_sheets.main import Pictron
import os
import json

# default non changing configurations for pictron
primary_config = {
    "page_size": (8.5, 11),
    "img_align_path": "answer_sheets/assets/images/checkerboard_144x_adj_color.jpg",
    "logo_path": "answer_sheets/assets/images/LiveTestLogo_144x.png",
    "bubble_shape": "circle",
    "bubble_ratio": 1,
    "font_path": "answer_sheets/assets/fonts/RobotoMono-Regular.ttf",
    "font_bold": "answer_sheets/assets/fonts/RobotoMono-Bold.ttf",
    "page_margins": (300, 100, 100, 50),
    "zebra_shading": False,
    "label_style": None,
    "que_ident_style": None,
    "font_alpha": 50,
    "outPath": "answer_sheets/generatedSheets/perfTEST",
    "outName": None,
}

with open(f"answer_sheets/perfect_configs.json", "r") as conf_file:
    config_templates = json.load(conf_file)


def find_best_config(num_questions:int, num_choices:int=5) -> dict:
    '''
    given a number of questions and choices. return the best configuration
    for the Pictron answer sheet generation possible. 
    '''
    if num_questions <= 0 or num_questions > 200:
        return False

    templates = config_templates[str(num_choices)]
    template_counts = (10, 20, 30, 40, 50, 75, 100, 150, 200)
    template = 0

    for question_count in template_counts:
        if num_questions <= question_count:
            template = question_count
            break

    for temp in templates:
        if int(temp['num_questions']) == template:
            return temp | primary_config



if __name__ == "__main__":
    best = find_best_config(38, 6)
    print(f"BEST: {best}")

    # best_config_ex = {
    #     "font_size": 40,
    #     "bubble_size": 95,
    #     "line_spacing": 180,
    #     "answer_spacing": 45,
    #     "label_spacing": 40, 
    #     "column_width": 205,
    #     "num_ans_options": 2,
    #     "num_questions": 10,
    # }
        
    pictron = Pictron(**best)
    pictron.generate(random_filled=True, course_name="Advanced Programming", test_name="Test 1: Syntax vs Semantics")
    print(os.getcwd())
    pictron.saveImage()
    



# {
    #     "font_size": 25,
    #     "bubble_size": 60,
    #     "line_spacing": 30,
    #     "column_width": 200,
    #     "answer_spacing": 40,
    #     "label_spacing": 45, 
    #     "num_ans_options": 2,
    #     "num_questions": 20,
    # },

