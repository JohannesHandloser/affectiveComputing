
from classifier.classification_handler import *
from helper.data_handler import *

if __name__ == "__main__":
    data_handler = DataHandler("zarok01")
    ch = ClassificationHandler(data_handler.data_dict)
    ch.classify("dt")
