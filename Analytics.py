from ScantronProcessor import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Analytics:
    def __init__(self):
        self.results = {}
        self.df_answers = pd.DataFrame()
        self.df_tests = pd.DataFrame()
        self.df_percentages = pd.DataFrame()
        self.num_questions = 0

    def create_df(self, test):
        temp = {k: v[1] for k, v in test.items()}
        self.df_answers = pd.DataFrame([temp])
        self.num_questions = len(self.df_answers.columns)


    def add_test(self, test):
        temp = {k: v[1] for k, v in test.items()}
        df = pd.DataFrame([temp])
        self.df_tests = pd.concat([self.df_tests, df], ignore_index=True)

    def find_percentages(self):
        num_students = len(analytics.df_tests)
        num_questions = len(analytics.df_tests.columns)
        tests = self.df_tests
        answers = self.df_answers

        percentages = []

        for i in range(1, num_questions+1):
            percentages.append(tests[i].value_counts()[answers[i][0]] / float(num_students) * 100)

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



answer_key = {
    1: (True, "A"),
    2: (True, "A"),
    3: (True, "C"),
    4: (True, "D"), 
    5: (True, "B"),
    6: (True, "B"),
    7: (True, "B"),
    8: (True, "D"),
    9: (True, "C"),
    10: (True, "C")
}

sns.set()
analytics = Analytics()
analytics.create_df(answer_key)

#   FAKE DATA ---------------------------------------

import random

dictionaries = []

for _ in range(100):
    dictionary = {}
    for i in range(1, 11):

        got_correct = random.randint(0, 100) > 30
        if got_correct:
            value = (True, analytics.df_answers[i][0])
        else:
            value = (random.choice([True, False]), random.choice(["A", "B", "C", "D"]))
        dictionary[i] = value
    dictionaries.append(dictionary)

# adding fake data to DF
for dic in dictionaries:
    analytics.add_test(dic)


analytics.find_percentages()
analytics.plot_percentages()
