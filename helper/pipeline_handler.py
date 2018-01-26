from classifier.classification_handler import *


class PipelineHandler:
    def __init__(self):
        self.data_handler = DataHandler()
        self.ch = ClassificationHandler()
        self.unprocessed_data = self.data_handler.unpreprocessed_data

    def pipeline_run(self, user="all", test_data_flag="all", type_of_classifier="dt", \
                     split_size=100, n_estimator=15, max_depth=10):
        data_dict = self.pipeline_data_preprocessing(user, test_data_flag)
        if type_of_classifier == "dt":
            self.ch.classify_dt(split_size, data_dict, test_data_flag)
            return self.ch.results
        elif type_of_classifier == "rf":
            self.ch.classify_rf(max_depth, n_estimator, data_dict, test_data_flag)
            return self.ch.results
        else:
            print("Only available classifier are dt and rf")

    def pipeline_data_preprocessing(self, user, test_data_flag):
        return self.data_handler.preprocessing_pipeline(self.data_handler.unpreprocessed_data, user, test_data_flag)

    def pipeline_list_of_runs(self, list_of_runs):
        run_results = dict()
        for run in list_of_runs:
            run_key =  "USER: " + run.user + " CL: " + run.type_of_classifier + " TESTDATA: " + run.test_data_flag
            if run.type_of_classifier == "dt":
                result = self.pipeline_run(run.user, run.test_data_flag, run.type_of_classifier, run.split_size)
                run_results[run_key + " SPLITSIZE: " + str(run.split_size)] = result
                self.ch.clear_results()
            elif run.type_of_classifier == "rf":
                result = self.pipeline_run(run.user, run.test_data_flag, run.type_of_classifier, run.n_estimator, run.max_depth)
                run_results[run_key + " ESTIMATOR: " + str(run.n_estimator) + " DEPTH: " + str(run.max_depth)] = result
                self.ch.clear_results()
        return run_results
