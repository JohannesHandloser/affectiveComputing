from helper.data_handler import *
from pca.pca_calculator import *

if __name__ == '__main__':


    data_handler = DataHandler()
    pca = PCA_Handler()
    print ("Calculate the Principal Component now")
    pca.calculate_principal_components(data_handler.data_frame)
    #print (data_handler.data_frame);
