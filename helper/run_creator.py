from helper.run import *
import random as r


class RunCreator:
    def __init__(self):
        self.users = ["1162656792", "punky_2002", "zarok01", "all"]
        self.test_data_sets = ["songs", "days", "all"]
        self.types_of_classifier = ["dt", "rf", "svm"]
        self.dt_hyperparameters = [100, 500, 1000, 5000]
        self.rf_hyperparameters = [10, 20, 30]
        self.svm_hyperparameters = ["linear", "rbf"]

    def create_random_run_list(self, number_of_runs):
        random_run_list = []
        i = 1
        while i < number_of_runs:
            type_of_classifier = r.choice(self.types_of_classifier)
            if type_of_classifier == "dt":
                run_obj = Run(user=r.choice(self.users), test_data_flag=r.choice(self.test_data_sets), \
                              type_of_classifier=type_of_classifier, split_size=r.choice(self.dt_hyperparameters))
            elif type_of_classifier == "rf":
                run_obj = Run(user=r.choice(self.users), test_data_flag=r.choice(self.test_data_sets), \
                              type_of_classifier=type_of_classifier, n_estimator=r.choice(self.rf_hyperparameters), \
                              max_depth=r.choice(self.rf_hyperparameters))
            elif type_of_classifier == "svm":
                run_obj = Run(user=r.choice(self.users), test_data_flag=r.choice(self.test_data_sets), \
                              type_of_classifier=type_of_classifier, kernel=self.svm_hyperparameters)
            else:
                # create run object with default parameters
                run_obj = Run(user=r.choice(self.users), test_data_flag=r.choice(self.test_data_sets))
            if run_obj in random_run_list:
                continue
            else:
                random_run_list.append(run_obj)
                i += 1
        return random_run_list


