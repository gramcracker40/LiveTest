from ScantronProcessor import *
import pandas as pd
import matplotlib.pyplot as plt

class Analytics:
    def __init__(self):
        self.results = {}
        self.df_answers = pd.DataFrame()
        self.df_tests = pd.DataFrame()
        self.df_percentages = pd.DataFrame()

    def create_df(self, test):
        temp = {k: v[1] for k, v in test.items()}
        self.df_answers = pd.DataFrame([temp])


    def add_test(self, test):
        temp = {k: v[1] for k, v in test.items()}
        df = pd.DataFrame([temp])
        self.df_tests = pd.concat([self.df_tests, df], ignore_index=True)

    def find_percentages(self):
        num_students = len(analytics.df_tests)
        num_questions = len(analytics.df_tests.columns)
        tests = self.df_tests
        answers = self.df_answers

        for i in range(1, num_questions+1):
            self.df_percentages[i] = [(tests[i].value_counts()[answers[i][0]] / float(num_students))]


    def plot_percentages(self):
        self.df_percentages.plot(kind='bar')
        plt.show()
        print(self.df_percentages)



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

results = {
    1: (True, "A"),
    2: (True, "A"),
    3: (True, "C"),
    4: (True, "D"), 
    5: (True, "B"),
    6: (True, "B"),
    7: (False, "A"),
    8: (True, "D"),
    9: (True, "C"),
    10: (True, "C")
}

results2 = {
    1: (True, "A"),
    2: (True, "A"),
    3: (False, "B"),
    4: (True, "D"), 
    5: (True, "B"),
    6: (True, "B"),
    7: (False, "A"),
    8: (True, "D"),
    9: (False, "A"),
    10: (True, "C")
}
analytics = Analytics()
analytics.create_df(answer_key)
analytics.add_test(results)
analytics.add_test(results2)

# print(analytics.df_tests.value_counts())

#   FAKE DATA ---------------------------------------

import random

dictionaries = []

for _ in range(25):
    dictionary = {}
    for i in range(1, 11):

        got_correct = random.randint(0, 10) > 2
        if got_correct:
            value = (True, analytics.df_answers[i][0])
        else:
            value = (random.choice([True, False]), random.choice(["A", "B", "C", "D"]))
        dictionary[i] = value
    dictionaries.append(dictionary)

for dic in dictionaries:
    analytics.add_test(dic)


print(analytics.df_tests)

analytics.find_percentages()
analytics.plot_percentages()
