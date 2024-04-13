'''
Purpose: to find the best templated configuration possible for the 
given number of questions and choices in usage with Pictron. 
'''
from answer_sheets.main import Pictron
import json

# default non changing configurations for pictron
primary_config = {
    "page_size": (8.5, 11),
    "img_align_path": "./assets/images/checkerboard_144x_adj_color.jpg",
    "logo_path": "./assets/images/LiveTestLogo_144x.png",
    "bubble_shape": "circle",
    "bubble_ratio": 1,
    "font_path": "./assets/fonts/RobotoMono-Regular.ttf",
    "font_bold": "./assets/fonts/RobotoMono-Bold.ttf",
    "page_margins": (300, 100, 100, 50),
    "zebra_shading": False,
    "label_style": None,
    "que_ident_style": None,
    "font_alpha": 50,
    "outPath": "./generatedSheets/perfTEST",
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




# best = find_best_config(89, 7)
# print(f"BEST: {best}")

# perf_conf_5 = {
#     {
#         "font_size": 40,
#         "bubble_size": 95,
#         "line_spacing": 180,
#         "answer_spacing": 45,
#         "label_spacing": 40, 
#         "column_width": 205,
#         "num_ans_options": 2,
#         "num_questions": 10,
#     },
#     {
#         "font_size": 25,
#         "bubble_size": 60,
#         "line_spacing": 30,
#         "column_width": 200,
#         "answer_spacing": 40,
#         "label_spacing": 45, 
#         "num_ans_options": 2,
#         "num_questions": 20,
#     },
 
# }

# for q_count in perf_conf_5:
#     perf_conf_5[q_count] |= primary_config
#     print(perf_conf_5[q_count])
#     pictron = Pictron(**perf_conf_5[q_count])
#     pictron.generate(random_filled=False)
#     pictron.saveImage()