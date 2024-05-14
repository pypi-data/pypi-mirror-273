import numpy as np
import matplotlib.pyplot as plt
# from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.signal import find_peaks
from va.utils.misc import out_json

class FSCChecks:
    def __init__(self, input_data):
        try:
            self.fsc_data = input_data['curves']['fsc']
        except KeyError as e:
            raise Exception(f"Error: Required data not found in the JSON file. {e}")

    def min_value(self):
        return np.min(self.fsc_data)

    def end_value(self):
        return self.fsc_data[-1]

    def min_final_diff_value(self):
        return self.end_value() - self.min_value()

    def large_drop_check(self, window_size=5, drop_threshold=0.7):
        max_gradient_change = 0
        for i in range(window_size, len(self.fsc_data)):
            window_data = self.fsc_data[i - window_size: i]
            if abs(window_data[-1] - window_data[0]) > drop_threshold:
                differences = np.diff(window_data)
                average_difference = np.mean(differences)
                max_gradient_change = max(max_gradient_change, abs(average_difference))
        return max_gradient_change

    def max_gradient_check(self, window_size=5):
        max_change = float('-inf')
        for i in range(window_size, len(self.fsc_data)):
            window_data = self.fsc_data[i - window_size: i]
            differences = np.diff(window_data)
            average_difference = np.mean(differences)
            max_change = max(max_change, abs(average_difference))
        return max_change

    def peak_finder(self, window_size=5):
        # smoothed_data = lowess(self.fsc_data, range(len(self.fsc_data)), frac=0.05)[:, 1]
        smoothed_data = np.convolve(self.fsc_data, np.ones(window_size) / window_size, mode='valid')
        peaks, _ = find_peaks(smoothed_data, distance=5, prominence=0.1)
        return len(peaks)

    def fsc_plotter(self, filepath):
        plt.figure()
        plt.plot(range(len(self.fsc_data)), self.fsc_data)
        plt.axhline(y=0, color='red', linestyle='--', label='Zero Line')
        plt.axhline(y=0.143, color='orange', linestyle='--', label='0.143 Line')
        plt.title(filepath)
        plt.savefig('{}.png'.format(filepath))
        plt.close()

    def fsc_checks(self, output_json):
        fsc_check = {}
        fsc_check['FSC'] = {}
        fsc_check['FSC']['minValue'] = self.min_value()
        fsc_check['FSC']['endValue'] = self.end_value()
        fsc_check['FSC']['peaks'] = self.peak_finder()
        fsc_check['FSC']['largestGradient'] = self.max_gradient_check()
        out_json(fsc_check, output_json)
