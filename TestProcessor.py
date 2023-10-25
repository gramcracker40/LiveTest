import os
from ScantronProcessor import ScantronProcessor

class TestProcessor:
    '''
    Given a directory full of scantrons for a specific test, 
        a 'Key' to the test, and the course_id.
    process a test and all of the submitted scantrons.
    '''

    def __init__(self, scantrons_dir:str, key:dict, course_id:int):
        '''
        Initialize a TestProcessor object that facilitates the idea
            of a test within the Scantron-Hacker. 

        Params:
            scantrons_dir: path to the directory holding all of the test's scantrons. 
            key: full path to the answer key's jpg/png
            course_id: id of the course you are adding the test to. 
        '''
        try:
            if os.path.exists(scantrons_dir) and os.path.isdir(scantrons_dir):
                # List all files in the directory
                self.file_paths = []
                for root, directories, files in os.walk(scantrons_dir):
                    for filename in files:
                        self.file_paths.append(os.path.join(root, filename))
            else:
                raise FileNotFoundError("The given scantrons_dir could not be located as a directory")

            
        
        except FileNotFoundError as err:
            print(err)


test = TestProcessor("FakeTest1", "real_examples/IMG_4162.jpg", 1)