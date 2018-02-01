import collections
import pyrebase

# Helper Class to connect to the firebase db and returns "pyrebase"-Objects from it
# handles authentication for firebase as well 
class Wrapper:
    config = {
        "apiKey": "AIzaSyASF2tTlD9AdK6Rsp4eTWuo1VOpRQ4WGX4",
        "authDomain": "emsplayer-95d89.firebaseapp.com",
        "databaseURL": "https://emsplayer-95d89.firebaseio.com",
        "storageBucket": "gs://emsplayer-95d89.appspot.com/"
    }

    def __init__(self):
        self.firebase = pyrebase.initialize_app(self.config)
        self.db = self.firebase.database()
        self.email = "emsplayer.ac1718@gmail.com"
        self.pw = "2pA-Ukw-7tK-8TE"

    def auth_and_login(self):
        self.auth = self.firebase.auth()
        self.user = self.auth.sign_in_with_email_and_password(self.email, self.pw)

    def refresh_auth(self):
        # before the 1 hour expiry:
        user = self.auth.refresh(self.user['refreshToken'])

    def get_data_from_pyrebase_object(self, entry):
        entry_val_obj = entry.val()
        emotionalstate_list = collections.OrderedDict(entry_val_obj["emotionalstate"])
        recommended_action = entry_val_obj["recommended_action"]

        gsr_resistance = []
        heart_beat_rate = []
        rr_rate = []
        motiontype = []
        skin_temp = []
        timestamps = [int(k) for k in emotionalstate_list.keys()]
        for emotionalstate in emotionalstate_list.values():
            gsr_resistance.append(emotionalstate["gsrResistance"])
            heart_beat_rate.append(emotionalstate["heartBeatRate"])
            rr_rate.append(emotionalstate["rrRate"])
            motiontype.append(emotionalstate["motiontypes"])
            skin_temp.append(emotionalstate["skinTemp"])

        return timestamps, gsr_resistance, heart_beat_rate, rr_rate, motiontype, skin_temp, recommended_action
