from firebase.firebase_wrapper import *
from helper.preprocessor import *
from classifier.classifier import *

if __name__ == '__main__':

    wrapper = Wrapper()
    preprocessor = Preprocessor()
    wrapper.auth_and_login()

    # recommended_action = 0
    node1 = wrapper.db.child("song_data_history").child("20171130182405_punky_2002").get()
    node2 = wrapper.db.child("song_data").child("punky_2002").get()
    #recommended_action = 1
    node3 = wrapper.db.child("song_data_history").child("20171130182659_punky_2002").get()


    data_list = [node1, node2, node3]



    for data in data_list:

        timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, \
        skin_temp, recommended_action = wrapper.get_data_from_pyrebase_object(data)

        preprocessor.calculate_feature_vector_list(timestamps, gsr_resistance, heart_beat_rate, \
                                               rr_rate, motiontype, skin_temp, recommended_action)

    classifier = Classifier(preprocessor.feature_vector_list)

    #classifier.do_PCA()

    classifier.plot_distr()










    #preprocessor.visualize_feature_vector_list(preprocessor.feature_vector_list)
















































