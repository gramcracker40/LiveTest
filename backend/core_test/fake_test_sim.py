from ScantronProcessor import ScantronProcessor
from TestProcessor import TestProcessor
import json

if __name__ == "__main__":
    key_path = "../../test_data/FakeTest1/IMG_4162.jpg"
    test1_path = "../../test_data/FakeTest1/IMG_4163.jpg"
    test2_path = "../../test_data/FakeTest1/IMG_4164.jpg"
    test3_path = "../../test_data/FakeTest1/IMG_4165.jpg"
    num_questions = 45

    key = TestProcessor.generate_key(key_path, num_questions)
    #del key[num_questions]
    print(json.dumps(key, indent=2))

    test1 = ScantronProcessor(test1_path, key)
    test2 = ScantronProcessor(test2_path, key)
    test3 = ScantronProcessor(test3_path, key)

    test1_results, test1_grade = test1.process(save_graded=True)
    test2_results, test2_grade = test2.process(save_graded=True)
    test3_results, test3_grade = test3.process(save_graded=True)

    print(f"\ntest1 grade: {test1_grade}\ntest2 grade: {test2_grade}\ntest3 grade: {test3_grade}\n")

    print("Test 1 results")
    print(test1_results)
    print("\n\n")

    print("Test 2 results")
    print(test2_results)
    print("\n\n")

    print("Test 3 results")
    print(test3_results)
    print("\n\n")