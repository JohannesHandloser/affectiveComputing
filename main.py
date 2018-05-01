from helper.pipeline_handler import *
import pprint
from helper.run import *
from helper.run_creator import *
from operator import getitem





if __name__ == "__main__":
    ph = PipelineHandler()
    list_of_runs = []
    list_of_runs.append(Run(user="all", test_data_flag="all", type_of_classifier="dummy",  strategy="uniform"))
    #list_of_runs.append(Run(user="all", test_data_flag="songs", type_of_classifier="dummy", strategy="stratified"))
    #list_of_runs.append(Run(user="all", test_data_flag="songs", type_of_classifier="dummy", strategy="most_frequent"))
    # list_of_runs.append(Run(user="1162656792", test_data_flag="all", type_of_classifier="dt", split_size=400))
    # list_of_runs.append(Run(user="1162656792", test_data_flag="songs", type_of_classifier="dt", split_size=400))
    # result = ph.pipeline_list_of_runs(list_of_runs)
    # pprint.pprint(result)

    #{'USER: punky_2002 CL: dummy TESTDATA: all STRATEGY: most_frequent': {'average': 0.52003750863685716}}
    #{'20180107': 0.87809293904646957, '20180108': 1.0, '20180119': 0.92771661081857348, 'average': 0.9352698499550144}

    #ph.order_result_dict_by_classification_rate(list_of_runs)


    #new_list = sorted(list_of_runs, key= lambda k: list(k.values())[0]["average"]  ,reverse=True)

    #
    # run_creator = RunCreator()
    # random_run_list = run_creator.create_random_run_list(10)
    # for run in random_run_list:
    #     pprint.pprint(run.__dict__, indent=5)


    pprint.pprint(ph.pipeline_list_of_runs(list_of_runs))









