from firebase.firebase_wrapper import *
from helper.preprocessor import *

if __name__ == '__main__':

    wrapper = Wrapper()
    wrapper.auth_and_login()
    node = wrapper.db.child("song_data_history").child("20171130182405_punky_2002").get()

    timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, \
    skin_temp, recommended_action = wrapper.get_data_from_pyrebase_object(node)

    preprocessor = Preprocessor()
    preprocessor.calculate_feature_vector_list(timestamps, gsr_resistance, heart_beat_rate, \
                                               rr_rate, motiontype, skin_temp, recommended_action)

    preprocessor.visualize_feature_vector_list(preprocessor.feature_vector_list)
















































