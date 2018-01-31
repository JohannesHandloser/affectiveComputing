class Run:
    def __init__(self, user="all", test_data_flag="all", type_of_classifier="dt", \
                 split_size=100, n_estimator=15, max_depth=10, kernel="linear", strategy="most_frequent"):
        self.user = user
        self.test_data_flag = test_data_flag
        self.type_of_classifier = type_of_classifier
        self.split_size = split_size
        self.n_estimator = n_estimator
        self.max_depth = max_depth
        self.kernel = kernel
        self.strategy = strategy

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
