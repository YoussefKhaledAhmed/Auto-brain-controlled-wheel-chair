from scipy.signal import butter, lfilter , filtfilt
import pandas as pd

class Filters:
    @staticmethod
    def butter_lowpass(cutoff , fs , order = 5):
        nyq = 0.5 * fs
        cutoff = cutoff / nyq
        return butter(order , cutoff , btype= 'low' , analog = False)

    @staticmethod
    def butter_lowpassFilter(data , cutoff , fs=128 , order = 5 , train = True):
        col_names = list(data.columns)
        if train:
            label = data[data.columns[-1]]
        try:
            data.drop(columns='Label', inplace=True)
        except KeyError:
            pass
        b, a = Filters.butter_lowpass(cutoff , fs , order = order)
        data = pd.DataFrame(filtfilt(b, a, data.transpose().to_numpy())).transpose()
        if train:
            data[data.columns[-1] + 1] = label
        data.columns = col_names
        return data

    @staticmethod
    def butter_highpass(cutoff , fs , order = 5):
        nyq = 0.5 * fs
        cutoff = cutoff / nyq
        return butter(order, cutoff, btype='high', analog=False)

    @staticmethod
    def butter_highpassFilter(data, cutoff, fs=128, order=5 , train = True):
        col_names = list(data.columns)
        if train:
            label = data[data.columns[-1]]
        try:
            data.drop(columns='Label', inplace=True)
        except KeyError:
            pass
        b, a = Filters.butter_highpass(cutoff, fs, order=order)
        data = pd.DataFrame(filtfilt(b, a, data.transpose().to_numpy())).transpose()
        if train:
            data[data.columns[-1] + 1] = label
        data.columns = col_names
        return data

    @staticmethod
    def butter_bandpass(lowcut , highcut, fs, order=5):
        nyq = 0.5 * fs
        lowcut = lowcut / nyq
        highcut = highcut / nyq
        return butter(order, [lowcut , highcut], btype='band')

    @staticmethod
    def butter_bandpassFilter(data, lowcut , highcut , fs = 128, order=5 , train = True):
        col_names = list(data.columns)
        if train:
            label = data[data.columns[-1]]
        try:
            data.drop(columns='Label', inplace=True)
        except KeyError:
            pass
        b, a = Filters.butter_bandpass(lowcut , highcut , fs , order=order)
        data = pd.DataFrame(filtfilt(b, a, data.transpose().to_numpy())).transpose()
        if train:
            data[data.columns[-1]+1] = label
        data.columns = col_names
        return data
