'''
Purpose: to find the best templated configuration possible for the 
given number of questions and choices in usage with Pictron. 
'''
from main import Pictron
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

with open(f"perfect_configs.json", "r") as conf_file:
    config_templates = json.load(conf_file)


def find_best_config(num_questions:int, num_choices:int=5):
    '''
    given a number of questions and choices. return the best configuration
    for the Pictron answer sheet generation possible. 
    '''
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




best = find_best_config(17, 4)
print(f"BEST: {best}")


# perf_conf_5 = {
#     10: {
#         "font_size": 24,
#         "bubble_size": 60,
#         "line_spacing": 35,
#         "answer_spacing": 100,
#         "label_spacing": 40, 
#         "num_ans_options": 6,
#         "num_questions": 10,
#     },
#     20: {
#         "font_size": 23,
#         "bubble_size": 55,
#         "line_spacing": 55,
#         "column_width": 120,
#         "answer_spacing": 30,
#         "label_spacing": 40, 
#         "num_ans_options": 6,
#         "num_questions": 20,
#     },
#     30: {
#         "font_size": 17,
#         "bubble_size": 41,
#         "line_spacing": 20,
#         "column_width": 90,
#         "answer_spacing": 30,
#         "label_spacing": 20, 
#         "num_ans_options": 6,
#         "num_questions": 30,
#     }, 
#     40: {
#         "font_size": 15,
#         "bubble_size": 36,
#         "line_spacing": 55,
#         "column_width": 70,
#         "answer_spacing": 25,
#         "label_spacing": 40, 
#         "num_ans_options": 6,
#         "num_questions": 40,
#     },
#     50: {
#         "font_size": 13,
#         "bubble_size": 30,
#         "line_spacing": 44,
#         "column_width": 85,
#         "answer_spacing": 45,
#         "label_spacing": 30, 
#         "num_ans_options": 6,
#         "num_questions": 50,
#     },
#     75: {
#         "font_size": 12,
#         "bubble_size": 25,
#         "line_spacing": 45,
#         "column_width": 70,
#         "answer_spacing": 25,
#         "label_spacing": 25, 
#         "num_ans_options": 6,
#         "num_questions": 75,
#     }, 
#     100: {
#         "font_size": 10,
#         "bubble_size": 22,
#         "line_spacing": 20,
#         "column_width": 65,
#         "answer_spacing": 40,
#         "label_spacing": 25,
#         "num_ans_options": 6,
#         "num_questions": 100,
#     },
#     150: {
#         "font_size": 8,
#         "bubble_size": 18,
#         "line_spacing": 20,
#         "column_width": 55,
#         "answer_spacing": 25,
#         "label_spacing": 25,
#         "num_ans_options": 6,
#         "num_questions": 150,
#     },
#     200: {
#         "font_size": 6,
#         "bubble_size": 14.5,
#         "line_spacing": 24,
#         "column_width": 45,
#         "answer_spacing": 14,
#         "label_spacing": 15,
#         "num_ans_options": 6,
#         "num_questions": 200,
#     }
# }

# for q_count in perf_conf_5:
#     perf_conf_5[q_count] |= primary_config
#     print(perf_conf_5[q_count])
#     pictron = Pictron(**perf_conf_5[q_count])
#     pictron.generate(random_filled=False)
#     pictron.saveImage()