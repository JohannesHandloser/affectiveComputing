
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd
from sklearn.decomposition import PCA # Choose a class of model by importing the appropriate estimator class
from sklearn import preprocessing


class PCA_Handler:

    def calculate_principal_components(self, matrixX):
        pca = PCA(n_components=2) # Choose the Hyperparameters
         # arrange data into feature matrix and target vector.

        x = matrixX.values #returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        df = pd.DataFrame(x_scaled)
        print ("Normalized Dataframe")
        print (df)

        pca.fit(df)

        print ("Principal Components")
        print(pca.components_)
        print ("Explained Variance")
        print(pca.explained_variance_)
