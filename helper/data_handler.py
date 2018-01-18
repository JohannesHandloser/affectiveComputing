import helper.preprocessor as preprocessor
import firebase.firebase_wrapper as wrapper
import pandas as pd


class DataHandler:

    def __init__(self, user):
        self.wrapper = wrapper.Wrapper()
        self.preprocessor = preprocessor.Preprocessor()
        self.wrapper.auth_and_login()
        self.preprocessing_pipeline(self.wrapper.db.child("song_data_history").get(), user)


    def get_track_days(self, all_entries, user):
        all_days = list()
        for entry in all_entries.each():
            time_string = entry.key()[:14]
            if int(time_string) > 20171123113603:
                track_day = entry.key()[:8]
                user_string = entry.key()[15:]
                if (user == "zarok01") & (user_string == "zarok01"):
                    if track_day not in all_days:
                        all_days.append(track_day)
                elif (user == "punky_2002") & (user_string == "punky_2002"):
                    if track_day not in all_days:
                        all_days.append(track_day)
                elif (user == "1162656792") & (user_string == "1162656792"):
                    if track_day not in all_days:
                        all_days.append(track_day)
                else:
                    if track_day not in all_days:
                        all_days.append(track_day)
        return all_days


    def create_data_dict(self, all_entries, all_days):
        data_dict = dict()
        for day in all_days:
            data_list = []
            for entry in all_entries.each():
                track_day = entry.key()[:8]
                if day == track_day:
                    data_list.append(entry)
            data_dict[day] = data_list
        return data_dict


    def create_data_frames_for_track_days(self, data_dict_tmp):
        data_dict = dict()
        for day, data_list in data_dict_tmp.items():
            for data in data_list:
                timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, \
                skin_temp, recommended_action = self.wrapper.get_data_from_pyrebase_object(data)
                self.preprocessor.calculate_feature_vector_list(timestamps, gsr_resistance, heart_beat_rate, \
                                                                       rr_rate, motiontype, skin_temp, recommended_action)

            data_frame = pd.DataFrame(self.preprocessor.feature_vector_list)
            data_frame.columns = ["M(GSR_Res)", "Std(GSR_Res)", "M(HBR)", "Std(HBR)", "M(RR)", "Std(RR)", \
                                  "M(Motion)", "Std(Motion)", "M(ST)", "Std(ST)", "MHR(RR)", "MRRI(RR)", "NN50(RR)", \
                                  "PNN50(RR)", "RMSSD(RR)", "SDNN(RR)", "RecommendedAct"]
            self.preprocessor.clear_feature_vector_list()
            data_dict[day] = data_frame
        return data_dict


    def preprocessing_pipeline(self, all_entries, user):
        track_days = self.get_track_days(all_entries, user)
        data_dict_tmp  = self.create_data_dict(all_entries, track_days)
        self.data_dict = self.create_data_frames_for_track_days(data_dict_tmp)














