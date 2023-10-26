import os, json
from ScantronProcessor import ScantronProcessor, find_and_rotate

class TestProcessor:
    '''
    Given a directory full of scantrons for a specific test, 
        a 'Key' to the test, and the course_id.
    process a test and all of the submitted scantrons.
    '''

    def __init__(self, scantrons_dir:str, key_path:dict, course_id:int, num_questions:int):
        '''
        Initialize a TestProcessor object that facilitates the idea
            of a test within the Scantron-Hacker. 

        Params:
            scantrons_dir: path to the directory holding all of the test's scantrons. 
            key: full path to the answer key's jpg/png
            course_id: id of the course you are adding the test to. 
        '''
        try:
            self.key = TestProcessor.generate_key(key_path, num_questions)
            self.course_id = course_id
            if os.path.exists(scantrons_dir) and os.path.isdir(scantrons_dir):
                # List all files in the directory
                self.file_paths = []
                for root, directories, files in os.walk(scantrons_dir):
                    for filename in files:
                        self.file_paths.append(os.path.join(root, filename))
                
                print(self.file_paths)
            else:
                raise FileNotFoundError("The given scantrons_dir could not be located as a directory")  
        
        except FileNotFoundError as err:
            print(err)


    @classmethod
    def generate_key(self, key_path:str, num_questions:int) -> {int:str}:
        '''
        given an image of a scantron key fully filled out, return the dictionary of answers
            can be use to generate a key out of an existing already filled out scantron. 
        '''
        key_results = {}

        key = ScantronProcessor(key_path, {x: None for x in range(num_questions)})
        key.image = find_and_rotate(key.image_path)        
        key.resize_image(1700, 4400)
        answers = key.detect_answers()

        print(f"#Answers: {len(answers)}")
        if num_questions < len(answers):
            answers = answers[len(answers) - num_questions + 1:]

        print(f"#Answers: {len(answers)}")
        answer_x_pairs = {
            "A" : (262, 402),
            "B" : (403, 557), 
            "C" : (519, 690), 
            "D" : (660, 825),
            "E" : (804, 950)
        }

        # build the key --> {1: 'A', 2: 'C', 3: 'E'}
        for count, (x,y,w,h) in enumerate(answers):
            # determine middle point of answer
            answered_middle = x + (w/2)
            
            # find what they answered from answer_x_pairs
            for val in answer_x_pairs:
                if (answered_middle >= answer_x_pairs[val][0]
                 and answered_middle <= answer_x_pairs[val][1]
                ):
                    key_results[count + 1] = val
                    break
        
        print(f"Key Results: {json.dumps(key_results, indent=2)}")
        return key_results

    def process(self) -> (list, float):
        '''
        process the test object. 
        '''
        self.test_results = []
        test_average = 0

        # loop through the file paths in the scantrons_dir
        for path in self.file_paths:
            ext = os.path.splitext(path)[-1]
            
            # extension check
            if ext in ['.jpg', '.png']:
                # grade the individual scantron
                temp = ScantronProcessor(path, self.key)
                graded_results, grade = temp.process()
                test_average += grade
                self.test_results.append(graded_results)
            else:
                return (None, "extension type must be 'png' or 'jpg' to be processed")
            
            
        return (self.test_results, test_average)
            

test = TestProcessor("FakeTest1", "real_examples/IMG_4162.jpg", 1, 45)
results, test_avg = test.process()

print(f"{json.dumps(results, indent=2)}\ntest_average: {test_avg}")