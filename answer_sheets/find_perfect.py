'''
Purpose: to find the best configuration possible for the given number of questions in usage with Pictron. 
'''
from main import Pictron

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


perf_conf = {
    10: {
        "font_size": 24,
        "bubble_size": 60,
        "line_spacing": 35,
        "answer_spacing": 100,
        "label_spacing": 40, 
        "num_ans_options": 5,
        "num_questions": 10,
    },
    20: {
        "font_size": 18,
        "bubble_size": 45,
        "line_spacing": 80,
        "answer_spacing": 30,
        "label_spacing": 40, 
        "num_ans_options": 5,
        "num_questions": 20,
    },
    30: {
        "font_size": 12,
        "bubble_size": 36,
        "line_spacing": 35,
        "column_width": 250,
        "answer_spacing": 30,
        "label_spacing": 20, 
        "num_ans_options": 5,
        "num_questions": 30,
    }, 
    39: {
        "font_size": 12,
        "bubble_size": 28,
        "line_spacing": 95,
        "column_width": 80,
        "answer_spacing": 25,
        "label_spacing": 40, 
        "num_ans_options": 5,
        "num_questions": 39,
    },
    75: {
        "font_size": 10,
        "bubble_size": 22,
        "line_spacing": 20,
        "column_width": 230,
        "answer_spacing": 27,
        "label_spacing": 40, 
        "num_ans_options": 5,
        "num_questions": 75,
    }, 
    100: {
        "font_size": 10,
        "bubble_size": 22,
        "line_spacing": 20,
        "column_width": 55,
        "answer_spacing": 15,
        "label_spacing": 25,
        "num_ans_options": 5,
        "num_questions": 100,
    }
}

for q_count in perf_conf:
    perf_conf[q_count] |= primary_config
    print(perf_conf[q_count])
    pictron = Pictron(**perf_conf[q_count])
    pictron.generate(random_filled=True)
    pictron.saveImage()