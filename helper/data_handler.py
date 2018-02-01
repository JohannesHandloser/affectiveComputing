import helper.preprocessor as preprocessor
import firebase.firebase_wrapper as wrapper
import pandas as pd
import collections

# Class to preprocess data in the wanted structur
class DataHandler:
    def __init__(self):
        self.wrapper = wrapper.Wrapper()
        self.preprocessor = preprocessor.Preprocessor()
        self.wrapper.auth_and_login()
        self.unpreprocessed_data = self.wrapper.db.child("song_data_history").get()

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
                elif (user == "all"):
                    if track_day not in all_days:
                        all_days.append(track_day)
        return all_days

    def create_data_dict_for_days(self, all_entries, all_days):
        data_dict = dict()
        for day in all_days:
            data_list = []
            for entry in all_entries.each():
                track_day = entry.key()[:8]
                if day == track_day:
                    data_list.append(entry)
            data_dict[day] = data_list
        return data_dict

    def create_data_dict_for_songs(self, all_entries, user):
        data_dict = dict()
        for entry in all_entries.each():
            time_string = entry.key()[:14]
            song_length = entry.val()["metadata"]["audiofeatures"]["durationMs"]
            track_length = len(entry.val()["emotionalstate"])
            if int(time_string) > 20171123113603 & song_length > 10000 & track_length > 20:
                user_string = entry.key()[15:]
                if (user == "zarok01") & (user_string == "zarok01"):
                    song_key, data_frame = self.helper_data_creation_song(entry)
                elif (user == "punky_2002") & (user_string == "punky_2002"):
                    song_key, data_frame = self.helper_data_creation_song(entry)
                elif (user == "1162656792") & (user_string == "1162656792"):
                    song_key, data_frame = self.helper_data_creation_song(entry)
                elif (user == "all"):
                    song_key, data_frame = self.helper_data_creation_song(entry)
                else:
                    continue
                data_dict[song_key] = data_frame
        return data_dict

    def helper_data_creation_song(self, entry):
        entry_val_obj = entry.val()
        time_string = entry.key()[:14]
        song_metadata_list = collections.OrderedDict(entry_val_obj["metadata"])
        song_key = song_metadata_list["song"] + " " + time_string
        timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, \
        skin_temp, recommended_action = self.wrapper.get_data_from_pyrebase_object(entry)
        self.preprocessor.calculate_feature_vector_list(timestamps, gsr_resistance, heart_beat_rate, \
                                                        rr_rate, motiontype, skin_temp, recommended_action)
        data_frame = pd.DataFrame(self.preprocessor.feature_vector_list)
        data_frame.columns = ["M(GSR_Res)", "Std(GSR_Res)", "M(HBR)", "Std(HBR)", "M(RR)", "Std(RR)", \
                              "M(Motion)", "Std(Motion)", "M(ST)", "Std(ST)", "MHR(RR)", "MRRI(RR)", "NN50(RR)", \
                              "PNN50(RR)", "RMSSD(RR)", "SDNN(RR)", "RecommendedAct"]
        self.preprocessor.clear_feature_vector_list()
        return song_key, data_frame

    def create_data_dict_for_track_days(self, data_dict_tmp):
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

    def create_data_for_cross_validation(self, all_entries, user):
        data_dict = dict()
        data_frame = pd.DataFrame()
        for entry in all_entries.each():
            time_string = entry.key()[:14]
            song_length = entry.val()["metadata"]["audiofeatures"]["durationMs"]
            track_length = len(entry.val()["emotionalstate"])
            if int(time_string) > 20171123113603 & song_length > 10000 & track_length > 20:
                user_string = entry.key()[15:]
                if (user == "zarok01") & (user_string == "zarok01"):
                    data_frame = pd.concat([data_frame, self.helper_create_data(entry)])
                elif (user == "punky_2002") & (user_string == "punky_2002"):
                    data_frame = pd.concat([data_frame, self.helper_create_data(entry)])
                elif (user == "1162656792") & (user_string == "1162656792"):
                    data_frame = pd.concat([data_frame, self.helper_create_data(entry)])
                elif (user == "all"):
                    data_frame = pd.concat([data_frame, self.helper_create_data(entry)])
        data_dict["all"] = data_frame
        return data_dict

    def helper_create_data(self, entry):
        timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, \
        skin_temp, recommended_action = self.wrapper.get_data_from_pyrebase_object(entry)
        self.preprocessor.calculate_feature_vector_list(timestamps, gsr_resistance, heart_beat_rate, \
                                                        rr_rate, motiontype, skin_temp, recommended_action)
        data_frame = pd.DataFrame(self.preprocessor.feature_vector_list)
        data_frame.columns = ["M(GSR_Res)", "Std(GSR_Res)", "M(HBR)", "Std(HBR)", "M(RR)", "Std(RR)", \
                              "M(Motion)", "Std(Motion)", "M(ST)", "Std(ST)", "MHR(RR)", "MRRI(RR)", "NN50(RR)", \
                              "PNN50(RR)", "RMSSD(RR)", "SDNN(RR)", "RecommendedAct"]
        self.preprocessor.clear_feature_vector_list()
        return data_frame

    def preprocessing_pipeline(self, all_entries, user, test_flag):
        if test_flag == "days":
            track_days = self.get_track_days(all_entries, user)
            data_dict_tmp = self.create_data_dict_for_days(all_entries, track_days)
            return self.create_data_dict_for_track_days(data_dict_tmp)
        elif test_flag == "songs":
            return self.create_data_dict_for_songs(all_entries, user)
        elif test_flag == "all":
            return self.create_data_for_cross_validation(all_entries, user)
