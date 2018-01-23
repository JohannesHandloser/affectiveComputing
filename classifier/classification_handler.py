from helper.data_handler import *
import sklearn.tree as tree
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


class ClassificationHandler:
    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.results = dict()

    def classify(self, type_of_classifier):
        track_days = list(self.data_dict.keys())
        for day in track_days:
            testdf = pd.DataFrame()
            traindf = pd.DataFrame()
            for key, value in self.data_dict.items():
                if day == key:
                    testdf = pd.concat([testdf, value])
                else:
                    traindf = pd.concat([traindf, value])
            self.do_training(type_of_classifier, testdf, traindf, day)
        mean = float(sum(self.results.values())) / len(self.results)
        self.results["average"] = mean


    def do_training(self, type_of_classifier, testdf, traindf, day):
        train_data_only = StandardScaler().fit_transform(traindf.iloc[:, :16])
        train_label = traindf.iloc[:, 16:]
        test_data_only = StandardScaler().fit_transform(testdf.iloc[:, :16])
        test_label = testdf.iloc[:, 16:]
        score = 0.0
        if type_of_classifier == "dt":
            dt = tree.DecisionTreeClassifier(min_samples_split=100)
            dt = dt.fit(train_data_only, train_label)
            score = dt.score(test_data_only, test_label)
        elif type_of_classifier == "rf":
            forest = RandomForestClassifier(max_depth=15, n_estimators=20, random_state=42)
            forest.fit(train_data_only, train_label)
            score = forest.score(test_data_only, test_label)
        self.results[day] = score








