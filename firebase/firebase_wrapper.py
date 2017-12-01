
import pyrebase
import requests

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
        entry_val_obj_key = entry.key()
        gsr_resistance = entry_val_obj["emotionalstate"]["gsrResistance"]
        rr_rate = entry_val_obj["emotionalstate"]["rrRate"]
        if "skinTemp" in entry_val_obj["emotionalstate"].keys():
            skin_temperature = entry_val_obj["emotionalstate"]["skinTemp"]
        else:
            skin_temperature = None
        heart_beat_rate = entry_val_obj["emotionalstate"]["heartBeatRate"]
        motiontypes = entry_val_obj["emotionalstate"]["motiontypes"]

        reward = entry_val_obj["reward"]

        playlist_nr = entry_val_obj["metadata"]["playlist"]
        #song_name = entry_val_obj["song"]

        return entry_val_obj_key, playlist_nr, reward, heart_beat_rate, \
               skin_temperature, rr_rate, gsr_resistance, motiontypes



    def put_action_on_firebase(self, key, data):
        self.db.child("return_action").child(key).set(data)





