import helper.preprocessor as preprocessor
import firebase.firebase_wrapper as wrapper
import pandas as pd


class DataHandler:


    def __init__(self, user):
        self.wrapper = wrapper.Wrapper()
        self.preprocessor = preprocessor.Preprocessor()
        self.wrapper.auth_and_login()
        self.read_out_entries(self.wrapper.db.child("song_data_history").get(), user)


    def read_out_entries(self, all_entries, user):
        data_list = []

        for entry in all_entries.each():
            user_string =  entry.key()[15:]
            if user == "all":
                data_list.append(entry)
            elif (user == "zarok01") & (user_string == "zarok01"):
                data_list.append(entry)
            elif (user == "punky_2002") & (user_string == "punky_2002"):
                data_list.append(entry)
            elif (user == "11127020586") & (user_string == "11127020586"):
                data_list.append(entry)
            elif (user == "1162656792") & (user_string == "1162656792"):
                data_list.append(entry)

        for data in data_list:
            timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, \
            skin_temp, recommended_action = self.wrapper.get_data_from_pyrebase_object(data)

            self.preprocessor.calculate_feature_vector_list(timestamps, gsr_resistance, heart_beat_rate, \
                                                       rr_rate, motiontype, skin_temp, recommended_action)


        # creates the whole pandas data Frame
        self.data_frame = pd.DataFrame(self.preprocessor.feature_vector_list)
        self.data_frame.columns = ["M(GSR_Res)", "Std(GSR_Res)", "M(HBR)", "Std(HBR)", "M(RR)", "Std(RR)", \
                                   "M(Motion)", "Std(Motion)", "M(ST)", "Std(ST)", "MHR(RR)", "MRRI(RR)", "NN50(RR)", \
                                   "PNN50(RR)", "RMSSD(RR)", "SDNN(RR)", "RecommendedAct"]








