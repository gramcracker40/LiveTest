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
        
        can be used to generate a key out of an existing already filled out scantron. 
        
        key_path -> absolute or relative path to the test's answer key image
                    the key simply needs to circle the correct answers and only
                    the correct answers. 
        num_questions -> ensures the key is properly generated.  
        '''

        key = ScantronProcessor(key_path, {x: None for x in range(num_questions)})
        key.image = find_and_rotate(key.image_path)        
        key.resize_image(1700, 4400)
        answers = key.detect_answers(num_questions)
        print(f"#Answers -> {len(answers)}")
        final_key = key.find_scantrons_answers(answers, num_questions)
        print("Final KEY:\n")
        print(json.dumps(final_key))
        return final_key

    def process(self) -> (list, float):
        '''
        process the test object. 
        open up every scantron image in the passed through scantrons_dir
        Build a temporary ScantronProcessor and grade the scantron in its entirety. 

        We can do something later so that the name of the scantrons image is 
        the M-number of the student so that they don't get improperly stored
        and we can tie the scantron object to a user.

        This function will process each of the scantrons using the passed key image. 
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
                print(f"{path} grade: {grade}")
                test_average += grade
                self.test_results.append(graded_results)
            else:
                return (None, "extension type must be 'png' or 'jpg' to be processed")
            
        print(f"test average {test_average/3}")
        print(f"test average len {test_average/len(self.file_paths)}") 
        return (self.test_results, round(test_average/len(self.file_paths), 2))
            

test = TestProcessor("FakeTest1", "real_examples/IMG_4162.jpg", 1, 45)
results, test_avg = test.process()

print(f"{json.dumps(results, indent=2)}\ntest_average: {test_avg}")