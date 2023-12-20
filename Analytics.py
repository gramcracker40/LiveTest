from backend.ScantronProcessor import *
from backend.TestProcessor import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys


class Analytics:
    def __init__(self):
        self.results = {}
        self.df_answers = pd.DataFrame()
        self.df_tests = pd.DataFrame()
        self.df_percentages = pd.DataFrame()
        self.num_questions = 0

    def create_df(self, test):
        tempAnswers = {k: v for k, v in test.items()}
        tempCorrect = {f"{k} Correct": v[0] for k, v in test.items()}
        complete = {**tempAnswers, **tempCorrect}
        self.df_answers = pd.DataFrame([complete])
        # self.df_answers = pd.DataFrame([test])
        self.num_questions = len(test)


    def add_test(self, test):
        tempAnswers = {k: v[1] for k, v in test.items()}
        tempCorrect = {f"{k} Correct": v[0] for k, v in test.items()}
        complete = {**tempAnswers, **tempCorrect}
        df = pd.DataFrame([complete])
        self.df_tests = pd.concat([self.df_tests, df], ignore_index=True)

    def find_percentages(self):
        num_students = len(self.df_tests)
        num_questions = self.num_questions
        tests = self.df_tests
        answers = self.df_answers

        percentages = []

        for i in range(1, num_questions+1):
            percentages.append((tests[f"{i} Correct"] == True).sum() / float(num_students) * 100)

        # sys.exit()

        p_dic = {
            "Question #": range(1, num_questions+1),
            "Percentage": percentages
        }

        self.df_percentages = pd.DataFrame(p_dic)


    def plot_percentages(self):
        plt.xlabel("Question Number")
        plt.ylabel("% Correct")
        plt.xticks(np.arange(1, self.num_questions+1))
        plt.yticks(np.arange(0, 100, 5))
        plt.bar(self.df_percentages["Question #"], self.df_percentages["Percentage"])
        plt.show()

    def save_question_pcts(self, testname):
        plt.xlabel("Question Number")
        plt.ylabel("% Correct")
        plt.xticks(np.arange(1, self.num_questions+1))
        plt.yticks(np.arange(0, 100, 5))
        plt.tight_layout()
        plt.bar(self.df_percentages["Question #"], self.df_percentages["Percentage"])
        plt.savefig(fname=f'question_percentages/{testname}.png')
    

key = TestProcessor.generate_key("real_examples/IMG_4162.jpg", 45)

analytics = Analytics()
analytics.create_df(key)

test = TestProcessor("FakeTest1", "real_examples/IMG_4162.jpg", 1, 45)
results, test_avg = test.process()

# adding fake data to DF
for dic in results:
    analytics.add_test(dic)


analytics.find_percentages()
analytics.plot_percentages()

# analytics.save_question_pcts('FakeTest1')


# answer_key = {
#     1: (True, "A"),
#     2: (True, "A"),
#     3: (True, "C"),
#     4: (True, "D"), 
#     5: (True, "B"),
#     6: (True, "B"),
#     7: (True, "B"),
#     8: (True, "D"),
#     9: (True, "C"),
#     10: (True, "C")
# }

# sns.set()
# analytics = Analytics()
# analytics.create_df(answer_key)

# #   FAKE DATA ---------------------------------------

# import random

# dictionaries = []

# for _ in range(100):
#     dictionary = {}
#     for i in range(1, 11):

#         got_correct = random.randint(0, 100) > 30
#         if got_correct:
#             value = (True, analytics.df_answers[i][0])
#         else:
#             value = (random.choice([True, False]), random.choice(["A", "B", "C", "D"]))
#         dictionary[i] = value
#     dictionaries.append(dictionary)

# # adding fake data to DF
# for dic in dictionaries:
#     analytics.add_test(dic)


# analytics.find_percentages()
# analytics.plot_percentages()
