import os, json
from core.ScantronProcessor import \
    ScantronProcessor, find_and_rotate, show_image

class TestProcessor:
    '''
    Given a directory full of scantrons for a specific test, 
        a 'Key' to the test, and the course_id.
    process a test and all of the submitted scantrons.
    '''

    def __init__(self, scantrons_dir:str, key_path:dict, num_questions:int, course_id:int=0):
        '''
        Initialize a TestProcessor object that facilitates the idea
            of a test within the Scantron-Hacker. 
        
        You must take a picture of the answer key and specify its path in 'key_path'

        Then have all of the pictures of scantrons in a single directory ie "user/test1"
            specify this folder with scantrons_dir. 
        
        You must also manually input the number of questions so ScantronProcessor can confirm
            its readings. 

        Later on the course_id will come into play when building the application

        Params:
            scantrons_dir: path to the directory holding all of the test's scantrons. 
            key: full path to the answer key's jpg/png
            course_id: id of the course you are adding the test to. 
        '''
        try:
            self.key = TestProcessor.generate_key(key_path, num_questions)
            self.course_id = course_id
            self.scantrons_dir = scantrons_dir

            # load all of the file paths in the scantrons_dir
            if os.path.exists(scantrons_dir) and os.path.isdir(scantrons_dir):
                self.file_paths = [os.path.join(root, filename) 
                    for root, directories, files in os.walk(scantrons_dir)
                    for filename in files]
            else:
                raise FileNotFoundError("The given 'scantrons_dir' could not be located as a directory")  
        
        except FileNotFoundError as err:
            print(err)

    @classmethod
    def generate_key(self, key_path:str, num_questions:int) -> {int:str}:
        '''
        given an image of a scantron key fully filled out, return the answers
          used to generate an answer key out of an existing already filled out scantron.
        
        key_path -> absolute path to the test's answer key image
                    the key simply needs to circle the correct answers and only
                    the correct answers. 
        num_questions -> ensures the key is properly generated.  
        returns: answer key --> {1: 'A', 2: 'B', 3: 'E'} 
        '''

        key = ScantronProcessor(key_path, {x: None for x in range(num_questions)})
        key.image = find_and_rotate(key.image_path)        
        key.resize_image(1700, 4400)
        answers = key.detect_answers(num_questions)
        final_key = key.find_scantrons_answers(answers, num_questions)
        final_key = {int(x): final_key[x] for x in final_key}
        show_image("answer-key-identified", key.image)
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

        returns: (test_results, test_average)
        test_results: list of the individual scantrons results that were processed for the test
        test_average: grade point average of the entire test. 

        '''
        self.test_results = []
        test_average = 0
        
        try:
            os.mkdir(f"{self.scantrons_dir}/graded")
        except FileExistsError:
            os.remove(f"{self.scantrons_dir}/graded")
            os.mkdir(f"{self.scantrons_dir}/graded")
        
        # loop through the file paths in the scantrons_dir
        for path in self.file_paths:
            ext = os.path.splitext(path)[-1]
            
            # extension check
            if ext in {'.jpg', '.png'}:
                # grade the individual scantron
                temp = ScantronProcessor(path, self.key)
                graded_results, grade = temp.process(
                    saved_location=f"{self.scantrons_dir}/graded/{path}", 
                    save_graded=True
                )
                # record the results and grade of the scantron. 
                test_average += grade
                self.test_results.append(graded_results)
            else:
                return (None, "extension type must be 'png' or 'jpg' to be processed")
            

        return (self.test_results, round(test_average/len(self.file_paths), 2))


if __name__ == "__main__":
    test = TestProcessor("../TestData/BatchOne/KEY1", "../TestData/BatchOne/KEY1.png", 30)
    results, test_avg = test.process()
    print(f"results: {results}\ntest average: {test_avg}")

# key = TestProcessor.generate_key("real_examples/IMG_4162.jpg", 45)
# print(key)