from hrv.classical import time_domain
import numpy as np
import math
from beautifultable import BeautifulTable

class Preprocessor:


    def __init__(self):
        self.feature_vector_list =[]
        self.target_vector_list =[]

    def calculate_target_vector_list(self, timestamps, gsr_resistance, heart_beat_rate, \
                                      rr_rate, motiontype, skin_temp, recommended_action):
        for i in range(0, len(timestamps) - 10):
            j = i+10
            self.target_vector_list.append(self.calculate_feature_vector(gsr_resistance[i:j], heart_beat_rate[i:j], \
                                                                          rr_rate[i:j], motiontype[i:j], skin_temp[i:j],\
                                                                          recommended_action))
           # self.calculate_rr_results(rr_rate[i:j])


    def calculate_feature_vector_list(self, timestamps, gsr_resistance, heart_beat_rate, \
                                      rr_rate, motiontype, skin_temp, recommended_action):
        for i in range(0, len(timestamps) - 10):
            j = i+10
            self.feature_vector_list.append(self.calculate_feature_vector(gsr_resistance[i:j], heart_beat_rate[i:j], \
                                                                          rr_rate[i:j], motiontype[i:j], skin_temp[i:j],\
                                                                          recommended_action))
            #self.calculate_rr_results(rr_rate[i:j])


    def calculate_feature_vector(self, gsr_resistance, heart_beat_rate, rr_rate, \
                                 motiontype, skin_temp, recommended_action):
        feature_vector = []
        feature_vector.append(self.calculate_mean(gsr_resistance))
        feature_vector.append(self.calculate_std(gsr_resistance))
        feature_vector.append(self.calculate_mean(heart_beat_rate))
        feature_vector.append(self.calculate_std(heart_beat_rate))
        feature_vector.append(self.calculate_mean(rr_rate))
        feature_vector.append(self.calculate_std(rr_rate))
        #feature_vector.append(self.calculate_rmssd(rr_rate))
        feature_vector.append(self.calculate_mean(motiontype))
        feature_vector.append(self.calculate_std(motiontype))
        feature_vector.append(self.calculate_mean(skin_temp))
        feature_vector.append(self.calculate_std(skin_temp))

        mhr, mrri, nn50, pnn50, rmssd, sdnn = self.calculate_rr_results(rr_rate)
        feature_vector.append(mhr)
        feature_vector.append(mrri)
        feature_vector.append(nn50)
        feature_vector.append(pnn50)
        feature_vector.append(rmssd)
        feature_vector.append(sdnn)

        feature_vector.append(recommended_action)
        return feature_vector



    def calculate_mean(self, data):
        mean = float(sum(data)) / float(len(data))
        return mean


    def calculate_std(self, data):
        std = np.std(data)
        return std


    #Variabilität der RR-Intervalle abnimmt -> Stress höher
    #Modalwert (Mo) steht für die häufigste gemessene Dauer eines RR-Intervalls
    #Die Amplitude des Modelwerts (AMo) beschreibt den prozentualen Anteil im Verhältnis zu allen erhobenen RR-Intervallen
    #Die Variabilitätsbreite (MxDMn) ist die Differenz zwischen dem maximalen und minimalen gemessenen RR-Intervall
    #AMo / 2Mo x MxDMn -> SI
    def calculate_braevsky_stress_index(self):
        si = 0.0
        return si


    # RMSSD, the root mean square of successive differences between adjacent R-R intervals
    def calculate_rmssd(self, rr_rate):
        rr_diff = []
        rr_sqdiff = []

        counter = 0
        while (counter < (len(rr_rate)) - 1):
            rr_diff.append(abs(rr_rate[counter] - rr_rate[counter + 1]))  # Calculate absolute difference between successive R-R interval
            rr_sqdiff.append(math.pow(rr_rate[counter] - rr_rate[counter + 1], 2))  # Calculate squared difference
            counter += 1
        rmssd = np.sqrt(np.mean(rr_sqdiff))  # Take root of the mean of the list of squared differences
        return rmssd

    #pnn50 ~ Prozentsatz der Intervalle mit mindestens 50 ms Abweichung vom vorausgehenden Intervall
    # (höhere Werte weisen auf vermehrte parasympathische Aktivität hin)
    #
    def calculate_rr_results(self, rr_rate):
        rr_rate_millisec = [x * 1000 for x in rr_rate]
        results  = time_domain(rr_rate_millisec)
        return results['mhr'], results['mrri'], results['nn50'], results['pnn50'], results['rmssd'], results['sdnn']













