from classifier.classification_handler import *
import copy as c
import time
from joblib import Parallel, delayed
import multiprocessing


# Class to handle the whole Pipeline Workflow
# Holds the unprocessed data from the firebase DB
# Has a parallized method to run the pipeline over the list of run objects
class PipelineHandler:
    def __init__(self):
        self.data_handler = DataHandler()
        self.ch = ClassificationHandler()
        self.unprocessed_data = self.data_handler.unpreprocessed_data

    def pipeline_run(self, user="all", test_data_flag="all", type_of_classifier="dt", \
                     split_size=100, n_estimator=15, max_depth=10, kernel="linear", strategy="most_frequent"):
        data_dict = self.pipeline_data_preprocessing(user, test_data_flag)
        if type_of_classifier == "dt":
            self.ch.classify_dt(split_size, data_dict, test_data_flag)
            return self.ch.results
        elif type_of_classifier == "rf":
            self.ch.classify_rf(max_depth, n_estimator, data_dict, test_data_flag)
            return self.ch.results
        elif type_of_classifier == "svm":
            self.ch.classify_svm(kernel, data_dict, test_data_flag)
            return self.ch.results
        elif type_of_classifier == "dummy":
            self.ch.classify_dummy(strategy, data_dict, test_data_flag)
            return self.ch.results
        else:
            print("Only available classifier are dt, rf and svm")

    def pipeline_data_preprocessing(self, user, test_data_flag):
        return self.data_handler.preprocessing_pipeline(self.data_handler.unpreprocessed_data, user, test_data_flag)

    def pipeline_list_of_runs(self, list_of_runs):
        num_cores = multiprocessing.cpu_count()
        print("Number of cores " + str(num_cores))
        time_start = time.time()
        run_results = Parallel(n_jobs=num_cores)(delayed(self.process_job)(run) for run in list_of_runs)
        time_end = time.time()
        print("Timediff: " + str(time_end - time_start))
        return self.order_result_dict_by_classification_rate(run_results)

    def process_job(self, run):
        run_key = "USER: " + run.user + " CL: " + run.type_of_classifier + " TESTDATA: " + run.test_data_flag
        if run.type_of_classifier == "dt":
            result = self.pipeline_run(run.user, run.test_data_flag, run.type_of_classifier, run.split_size)
            result_copy = c.deepcopy(result)
            self.ch.clear_results()
            return {run_key + " SPLITSIZE: " + str(run.split_size): result_copy}
        elif run.type_of_classifier == "rf":
            result = self.pipeline_run(run.user, run.test_data_flag, run.type_of_classifier, run.n_estimator,
                                       run.max_depth)
            result_copy = c.deepcopy(result)
            self.ch.clear_results()
            return {run_key + " ESTIMATOR: " + str(run.n_estimator) + " DEPTH: " + str(run.max_depth): result_copy}
        elif run.type_of_classifier == "svm":
            result = self.pipeline_run(run.user, run.test_data_flag, run.type_of_classifier, run.kernel)
            result_copy = c.deepcopy(result)
            self.ch.clear_results()
            return {run_key + " KERNEL: " + run.kernel: result_copy}
        elif run.type_of_classifier == "dummy":
            result = self.pipeline_run(run.user, run.test_data_flag, run.type_of_classifier, run.strategy)
            result_copy = c.deepcopy(result)
            self.ch.clear_results()
            return {run_key + " STRATEGY: " + run.strategy: result_copy}

    def order_result_dict_by_classification_rate(self, run_results):
        ordered_list = sorted(run_results, key=lambda k: list(k.values())[0]["average"], reverse=True)
        return ordered_list
