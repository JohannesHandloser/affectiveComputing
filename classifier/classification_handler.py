import sklearn.tree as tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from helper.data_handler import *
from sklearn import svm
from sklearn.dummy import DummyClassifier


# Class to handle the different Classificators
# Available are SVM, Decision Tree, Random Forest, Dummy Classifier
# Is able to deal with different hyperparameter settings given by the pipeline
class ClassificationHandler:
    def __init__(self):
        self.results = dict()
        self.dummyClassifierResults = dict()

    def do_training_dt(self, testdf, traindf, track, split_size):
        train_data_only = MinMaxScaler().fit_transform(traindf.iloc[:, :16])
        train_label = traindf.iloc[:, 16:]
        test_data_only = MinMaxScaler().fit_transform(testdf.iloc[:, :16])
        test_label = testdf.iloc[:, 16:]
        dt = tree.DecisionTreeClassifier(min_samples_split=split_size)
        dt = dt.fit(train_data_only, train_label)
        score = dt.score(test_data_only, test_label)
        self.results[track] = score

    def do_training_rf(self, testdf, traindf, track, max_depth, estimators):
        train_data_only = MinMaxScaler().fit_transform(traindf.iloc[:, :16])
        train_label = traindf.iloc[:, 16:]
        test_data_only = MinMaxScaler().fit_transform(testdf.iloc[:, :16])
        test_label = testdf.iloc[:, 16:]
        forest = RandomForestClassifier(max_depth=max_depth, n_estimators=estimators, random_state=42)
        forest.fit(train_data_only, train_label)
        score = forest.score(test_data_only, test_label)
        self.results[track] = score

    def do_training_svm(self, testdf, traindf, track, kernel):
        train_data_only = MinMaxScaler().fit_transform(traindf.iloc[:, :16])
        train_label = traindf.iloc[:, 16:]
        test_data_only = MinMaxScaler().fit_transform(testdf.iloc[:, :16])
        test_label = testdf.iloc[:, 16:]
        svc = svm.SVC(kernel=kernel, C=1, gamma=0.7)
        svc = svc.fit(train_data_only, train_label)
        score = svc.score(test_data_only, test_label)
        self.results[track] = score

    def do_training_dummy_classifier(self, testdf, traindf, data, strategy):
        train_data_only = MinMaxScaler().fit_transform(traindf.iloc[:, :16])
        train_label = traindf["RecommendedAct"].values.tolist()
        test_data_only = MinMaxScaler().fit_transform(testdf.iloc[:, :16])
        test_label = testdf["RecommendedAct"].values.tolist()
        dummy_cl = DummyClassifier(strategy=strategy, random_state=None, constant="constant")
        dummy_cl.fit(train_data_only, train_label, sample_weight=None)
        score = dummy_cl.score(test_data_only, test_label)
        self.results[data] = score

    def classify_dummy(self, strategy, data_dict, test_flag):
        if test_flag == "days" or test_flag == "songs":
            test_data = list(data_dict.keys())
            for data in test_data:
                testdf = pd.DataFrame()
                traindf = pd.DataFrame()
                for key, value in data_dict.items():
                    if data == key:
                        testdf = pd.concat([testdf, value])
                    else:
                        traindf = pd.concat([traindf, value])
                self.do_training_dummy_classifier(testdf, traindf, data, strategy)
            mean = float(sum(self.results.values())) / len(self.results)
            self.results["average"] = mean
        else:
            df = pd.DataFrame()
            for key, value in data_dict.items():
                df = pd.concat([df, value])
            traindf, testdf = train_test_split(df, test_size=0.2)
            self.do_training_dummy_classifier(testdf, traindf, "average", strategy)

    def classify_dt(self, split_size, data_dict, test_flag):
        if test_flag == "days" or test_flag == "songs":
            test_data = list(data_dict.keys())
            for data in test_data:
                testdf = pd.DataFrame()
                traindf = pd.DataFrame()
                for key, value in data_dict.items():
                    if data == key:
                        testdf = pd.concat([testdf, value])
                    else:
                        traindf = pd.concat([traindf, value])
                self.do_training_dt(testdf, traindf, data, split_size)
            mean = float(sum(self.results.values())) / len(self.results)
            self.results["average"] = mean
        else:
            df = pd.DataFrame()
            for key, value in data_dict.items():
                df = pd.concat([df, value])
            traindf, testdf = train_test_split(df, test_size=0.2)
            self.do_training_dt(testdf, traindf, "average", split_size)

    def classify_rf(self, max_depth, estimators, data_dict, test_flag):
        if test_flag == "days" or test_flag == "songs":
            test_data = list(data_dict.keys())
            for data in test_data:
                testdf = pd.DataFrame()
                traindf = pd.DataFrame()
                for key, value in data_dict.items():
                    if data == key:
                        testdf = pd.concat([testdf, value])
                    else:
                        traindf = pd.concat([traindf, value])
                self.do_training_rf(testdf, traindf, data, max_depth, estimators)
            mean = float(sum(self.results.values())) / len(self.results)
            self.results["average"] = mean
        else:
            df = pd.DataFrame()
            for key, value in data_dict.items():
                df = pd.concat([df, value])
            traindf, testdf = train_test_split(df, test_size=0.2)
            self.do_training_rf(testdf, traindf, "average", max_depth, estimators)

    def classify_svm(self, kernel, data_dict, test_flag):
        if test_flag == "days" or test_flag == "songs":
            test_data = list(data_dict.keys())
            for data in test_data:
                testdf = pd.DataFrame()
                traindf = pd.DataFrame()
                for key, value in data_dict.items():
                    if data == key:
                        testdf = pd.concat([testdf, value])
                    else:
                        traindf = pd.concat([traindf, value])
                self.do_training_svm(testdf, traindf, data, kernel)
            mean = float(sum(self.results.values())) / len(self.results)
            self.results["average"] = mean
        else:
            df = pd.DataFrame()
            for key, value in data_dict.items():
                df = pd.concat([df, value])
            traindf, testdf = train_test_split(df, test_size=0.2)
            self.do_training_svm(testdf, traindf, "average", kernel)

    def clear_results(self):
        self.results.clear()
