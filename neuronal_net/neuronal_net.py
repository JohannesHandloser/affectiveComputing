
from firebase.firebase_wrapper import *
from learner.preprocessor import *

class NeuronalNet:

    def __init__(self,wrapper,preprocessor):
        self.wrapper = wrapper
        self.preprocessor = preprocessor
        self.entry_counter = 0

        self.all_pyres = []
        self.getAllEntries()

    def getAllEntries(self):
        # first data set
        self.all_entries = self.wrapper.db.child("song_data").child("punky_2002").get()

        # second data set with ones
        # wrapper.db.child("song_data_history").child("20171130182659_punky_2002").get()

        # third data set with zeros
        # wrapper.db.child("song_data_history").child("20171130182405_punky_2002").get()

        timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, skin_temp, recommended_action = self.wrapper.get_data_from_pyrebase_object(self.all_entries)
        self.preprocessor.calc_new_table(timestamps,gsr_resistance,heart_beat_rate,rr_rate,motiontype,skin_temp,recommended_action)
