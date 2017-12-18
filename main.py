from firebase.firebase_wrapper import *
from helper.preprocessor import *
from classifier.classifier import *

if __name__ == '__main__':

    wrapper = Wrapper()
    preprocessor = Preprocessor()
    wrapper.auth_and_login()


    data_list = []

    all_entries = wrapper.db.child("song_data_history").get()
    for entry in all_entries.each():
        entry_key = entry.key()
        if "11127020586" in entry_key:
            data_list.append(entry)

    for data in data_list:
        timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, \
        skin_temp, recommended_action = wrapper.get_data_from_pyrebase_object(data)

        preprocessor.calculate_feature_vector_list(timestamps, gsr_resistance, heart_beat_rate, \
                                                   rr_rate, motiontype, skin_temp, recommended_action)
    #
    # feature_matrix = pd.DataFrame(preprocessor.feature_vector_list)
    # feature_matrix.columns = ["M(GSR_Res)", "Std(GSR_Res)", "M(HBR)", "Std(HBR)", "M(RR)", "Std(RR)", \
    #                           "RMSSD(RR)", "M(Motion)", "Std(Motion)", "M(ST)", "Std(ST)", "Classified"]



    classifier = Classifier(preprocessor.feature_vector_list)
    classifier.do_PCA()













    #preprocessor.visualize_feature_vector_list(preprocessor.feature_vector_list)
















































