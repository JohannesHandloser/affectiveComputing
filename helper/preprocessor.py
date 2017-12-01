import statistics
import numpy as np
import math

class Preprocessor:

    # baevsky stress index (SI) -> aus RR rate berechnen
    # modalwert -> am häufigsten aufgetretene wert

    def calculate_feature_vector(self, playlist_nr, motiontypes, heart_beat_rate, \
                                 skin_temperature, rr_rate, gsr_resistance):
        feature_vector = []
        # data = heart_beat_rate, rr_rate, skin_temperature, gsr_resistance (all preprocessed)
        counter = 1
        for data in self.preprocess_raw_data(heart_beat_rate, rr_rate, skin_temperature, gsr_resistance, motiontypes):
            feature_vector.append(self.calculate_mean(data))
            feature_vector.append(self.calculate_std(data))

            if counter == 2:
                feature_vector.append(self.calculate_rmssd(list(data.values())))
            counter += 1

        feature_vector.append(playlist_nr)
        return feature_vector


    def calculate_mean(self, data):
        if isinstance(data, dict):
            numbers = [data[key] for key in data]
            mean = statistics.mean(numbers)
        else:
            mean = float(sum(data)) / float(len(data))
        return mean


    def calculate_std(self, data):
        if isinstance(data, dict):
            test = list(data.values())
            std = np.std(test)
        else:
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
        # TODO set default value if rr_rate contains only 1 or 0 entries

        return rmssd


    def preprocess_raw_data(self, heart_beat_rate, rr_rate, skin_temperature, gsr_resistance, motiontypes):
        heart_beat_rate_prepro = {int(k): float(v) for k, v in heart_beat_rate.items()}
        rr_interval_prepro = {int(k): float(v) for k, v in rr_rate.items()}
        if skin_temperature is not None:
            skin_temperature_prepro = {int(k): float(v) for k, v in skin_temperature.items()}
        else:

            # TODO think of some better handling for skin_temperature = None
            skin_temperature_prepro = [27.0]
        gsr_resistance_prepro = {int(k): float(v) for k, v in gsr_resistance.items()}
        motiontypes_prepro = {int(k): float(v) for k, v in motiontypes.items()}
        return heart_beat_rate_prepro, rr_interval_prepro, \
               skin_temperature_prepro, gsr_resistance_prepro, motiontypes_prepro





    def stream_handler(self, message):
        print(message["data"])
        print(message["event"])






