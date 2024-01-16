from ScantronProcessor import ScantronProcessor
from TestProcessor import TestProcessor
import json

if __name__ == "__main__":
    key_path = "../../test_data/BatchOne/KEY1.png"
    test1_path = "/home/bench/answer_key_app/test_data/BatchOne/KEY1/IMG_8750.png"
    test2_path = "/home/bench/answer_key_app/test_data/BatchOne/KEY1/IMG_8752.png"
    num_questions = 31

    key = TestProcessor.generate_key(key_path, num_questions)
    del key[num_questions]
    print(json.dumps(key, indent=2))

    test1 = ScantronProcessor(test1_path, key)
    test2 = ScantronProcessor(test2_path, key)

    
    test1_results, test1_grade = test1.process(
        saved_location=f"Graded-Located", save_graded=True
    )
    test2_results, test2_grade = test2.process(
        saved_location=f"Graded-Located", save_graded=True
    )

    print(f"test1 grade: {test1_grade}\ntest2 grade: {test2_grade}")