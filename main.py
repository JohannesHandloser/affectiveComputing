from helper.pipeline_handler import *
import pprint
from helper.run import *

if __name__ == "__main__":
    ph = PipelineHandler()
    list_of_runs = []
    # list_of_runs.append(Run(user="zarok01", test_data_flag="days", type_of_classifier="dt", split_size=200))
    # list_of_runs.append(Run(user="1162656792", test_data_flag="days", type_of_classifier="rf", n_estimator=10, max_depth=20))
    # list_of_runs.append(Run(user="1162656792", test_data_flag="all", type_of_classifier="dt", split_size=400))
    list_of_runs.append(Run(user="1162656792", test_data_flag="songs", type_of_classifier="dt", split_size=400))


    result = ph.pipeline_list_of_runs(list_of_runs)
    pprint.pprint(result)






