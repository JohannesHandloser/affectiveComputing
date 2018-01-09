

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.svm import SVC # "Support vector classifier" # choose the model

class SupportVectorMachine_Handler:

    def performSVM(self,matrixX,targeValues):
        model = SVC(kernel='linear', C=1E10)
        model.fit(matrixX,targeValues) # Matrix + Target Vector
        print (model.support_vectors_)
