import helper.preprocessor as preprocessor
import firebase.firebase_wrapper as wrapper
import pandas as pd


class DataHandler:


    def __init__(self, user, daily_target, day_string=""):
        self.wrapper = wrapper.Wrapper()
        self.preprocessor = preprocessor.Preprocessor()
        self.wrapper.auth_and_login()
        self.read_out_entries(self.wrapper.db.child("song_data_history").get(), user, daily_target, day_string)


    def read_out_entries(self, all_entries, user, daily_target, day_string):
        data_list = []
        target_list = []

        for entry in all_entries.each():
            time_string = entry.key()[:14]
            if int(time_string) > 20171123113603:
                track_day = entry.key()[:8]
                user_string =  entry.key()[15:]
                if user == "all":
                    if daily_target:
                        if day_string == track_day:
                            target_list.append(entry)
                        else:
                            data_list.append(entry)
                    else:
                        data_list.append(entry)
                elif (user == "zarok01") & (user_string == "zarok01"):
                    if daily_target:
                        if day_string == track_day:
                            target_list.append(entry)
                        else:
                            data_list.append(entry)
                    else:
                        data_list.append(entry)
                elif (user == "punky_2002") & (user_string == "punky_2002"):
                    if daily_target:
                        if day_string == track_day:
                            target_list.append(entry)
                        else:
                            data_list.append(entry)
                    else:
                        data_list.append(entry)
                elif (user == "11127020586") & (user_string == "11127020586"):
                    if daily_target:
                        if day_string == track_day:
                            target_list.append(entry)
                        else:
                            data_list.append(entry)
                    else:
                        data_list.append(entry)
                elif (user == "1162656792") & (user_string == "1162656792"):
                    if daily_target:
                        if day_string == track_day:
                            target_list.append(entry)
                        else:
                            data_list.append(entry)
                    else:
                        data_list.append(entry)

        for data in data_list:
            timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, \
            skin_temp, recommended_action = self.wrapper.get_data_from_pyrebase_object(data)

            self.preprocessor.calculate_feature_vector_list(timestamps, gsr_resistance, heart_beat_rate, \
                                                       rr_rate, motiontype, skin_temp, recommended_action)

        if daily_target:
            for target in target_list:
                timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, \
                skin_temp, recommended_action = self.wrapper.get_data_from_pyrebase_object(target)

                self.preprocessor.calculate_target_vector_list(timestamps, gsr_resistance, heart_beat_rate, \
                                                rr_rate, motiontype, skin_temp, recommended_action)

            self.test_data = pd.DataFrame(self.preprocessor.target_vector_list)
            self.test_data.columns = ["M(GSR_Res)", "Std(GSR_Res)", "M(HBR)", "Std(HBR)", "M(RR)", "Std(RR)", \
                                       "M(Motion)", "Std(Motion)", "M(ST)", "Std(ST)", "MHR(RR)", "MRRI(RR)", "NN50(RR)", \
                                       "PNN50(RR)", "RMSSD(RR)", "SDNN(RR)", "RecommendedAct"]



        # creates the whole pandas data Frame
        self.data_frame = pd.DataFrame(self.preprocessor.feature_vector_list)
        self.data_frame.columns = ["M(GSR_Res)", "Std(GSR_Res)", "M(HBR)", "Std(HBR)", "M(RR)", "Std(RR)", \
                                   "M(Motion)", "Std(Motion)", "M(ST)", "Std(ST)", "MHR(RR)", "MRRI(RR)", "NN50(RR)", \
                                   "PNN50(RR)", "RMSSD(RR)", "SDNN(RR)", "RecommendedAct"]








