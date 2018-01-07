import helper.preprocessor as preprocessor
import firebase.firebase_wrapper as wrapper
import pandas as pd


class DataHandler:


    def __init__(self):
        self.wrapper = wrapper.Wrapper()
        self.preprocessor = preprocessor.Preprocessor()
        self.read_out_entries(self.wrapper.db.child("song_data_history").get())

        # split data table into data X and class labels y
        self.data = self.data_frame.ix[:, 0:10].values
        self.label = self.data_frame.ix[:, 11].values
        #print (self.data)
        #print (self.label)

    def read_out_entries(self, all_entries):
        data_list = []

        for entry in all_entries.each():
            date_string = entry.key()[:14]
            #if int(date_string) >= 20171129224345:
            data_list.append(entry)

        for data in data_list:
            #print ("Iteration for Data")
            print (data)
            timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, \
            skin_temp, recommended_action = self.wrapper.get_data_from_pyrebase_object(data)

            self.preprocessor.calculate_feature_vector_list(timestamps, gsr_resistance, heart_beat_rate, \
                                                       rr_rate, motiontype, skin_temp, recommended_action)


        # creates the whole pandas data Frame
        self.data_frame = pd.DataFrame(self.preprocessor.feature_vector_list)
        self.data_frame.columns = ["M(GSR_Res)", "Std(GSR_Res)", "M(HBR)", "Std(HBR)", "M(RR)", "Std(RR)", \
                                   "M(Motion)", "Std(Motion)", "M(ST)", "Std(ST)", "MHR(RR)", "MRRI(RR)", "NN50(RR)", \
                                   "PNN50(RR)", "RMSSD(RR)", "SDNN(RR)", "RecommendedAct"]
