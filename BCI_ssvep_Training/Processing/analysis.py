import math
import sklearn
import pickle
import pandas as pd
import scipy.signal as signal
from Processing.Filter import Filters
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class staticSpectralAnalysis:
    @staticmethod
    def CAR(Data: pd.DataFrame):
        """
        @TODO: this is a function to apply "Common Average Reference"
        :param Data: the data of one trial which needs "CAR"
        :return: the same Data but after applying the CAR to it
        """
        # so, basically CAR is based on subtracting the mean of each chanel through
        #     the whole trial from each row of data
        mean = Data.mean(axis = 1) # mean of the data along each electrode.
        for col in Data.columns[:-1]: # [:-1] will asure that the label isn't included.
            Data[col] = Data[col] - mean
        return Data

    @staticmethod
    def welch(data , timeOfOneEpoch:int = 5 , FS: int = 128 ,visualize = False, train = True):
        """
        @TODO: this is a function to apply "welch's" method on the data.
        :param data: EEG signal in the DataFrame form with (no.of samples * no. of channels).
        :param timeOfOneEpoch: is the time where single segment of data (i.e. epoch or trial) recorded at.
        :param FS: it's the sampling frequency.
        :param visualize: if u need to visualize the result from welch's method.
        :param train: if this is a data to train the ML model (i.e. it contains label).
        :return: Power and frequencies arrays with the label.
        """
        """
        steps:
        1. dropping the column with the 'Label' name if this data is for training otherwise there shouldn't 
           be the label column.
        2. applying the welch on each channel separately then appending the results in lists
        """
        freqList = []
        powerList = []
        if train:
            label = data['Label'].iloc[0]
            # dropping the data from the data and saving the result in the same data
            data.drop(columns = 'Label' , inplace = True)

        for ch in data.columns.tolist():
            f , Pxx_den = signal.welch(data[ch].to_numpy() , fs = FS , nperseg = timeOfOneEpoch * FS)
            freqList.append(f)
            powerList.append(Pxx_den)

        freqResolution = freqList[0][1] - freqList[0][0]

        if visualize:
            return freqList , powerList , label
        elif train:
            return powerList , label
        else:
            return powerList , freqResolution


    def welch_file(self , df, flickering_time , visualize = False, train = True):
        """
        @TODO: this function computes the welch for the whole file
               through extracting each trial computing the welch then appending
               the result of each trial
        :param df: dataFrame of the whole file
        :param flickering_time: time of each trial in seconds
        :param visualize:
        :param train:
        :return return_data: output of the welch's method for each trial
                             where its shape:
                             return_data[number_of_trial][freq or power or label][channel_number]
        """
        return_data = list()
        file_len = df.shape[0]
        samples = flickering_time * 128
        number_of_trials = int(file_len / samples)
        for i in range(number_of_trials):
            df_temp = df.iloc[i * samples:(i + 1) * samples, :]
            return_data.append(self.welch(df_temp , visualize=visualize , train=train))
        return return_data



    @staticmethod
    def featureExtraction_welch(welch_output, harmonic_num, channel = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4'] , train = True):
        """
        @TODO: it calculates the welch of the whole file and
               from welch, power range of interested frequencies are extracted
        :param welch_output: list of tuple, tuple(power,label) one for each trial.
        :param harmonic_num: int (2nd-3rd) hramonic of main frequencies.
        :param channel: list of channels.
        :param train: if True then label is taken in consideration otherwise then not.
        :return: list of list for each trial and list for labels.
        """
        X = list()
        lable = list()

        if train:
            frequency_resolution = 0.2
        else:
            frequency_resolution = welch_output[1]


        if harmonic_num == 2:
            adaptave_freq = [6.6, 7.6, 8.6, 10.0, 12.0, 13.2, 15.2, 17.2, 20, 24]
        else:
            adaptave_freq = [6.6, 7.6, 8.6, 10.0, 12.0, 13.2, 15.2, 17.2, 20, 24, 19.8, 22.8, 25.8, 30, 36]

        channels_def = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

        for i in range(len(welch_output)):  # loop over trials
            features_trial = list()
            if train:
                Pxx_den = welch_output[i][0]
                lable.append(welch_output[i][1])
            else:
                Pxx_den = welch_output[0]

            for ch in channel:  # loop over channels
                index_pos = channels_def.index(ch)
                features_ch = list()
                for f in adaptave_freq:
                    idx = math.ceil(f / frequency_resolution)
                    features_ch += Pxx_den[index_pos][idx - 2:idx + 3].tolist()
                features_trial += features_ch
            X.append(features_trial)
        if train:
            return X, lable
        else:
            return X

class multivariateComponentsAnalysis:
    @staticmethod
    def labelEncoder(features , labels , train_size = 0.8):
        labelEncoder = LabelEncoder()
        encodedLabels = labelEncoder.fit_transform(labels)
        x_train, x_test, y_train, y_test = train_test_split(features,
                                                       encodedLabels, random_state=None, train_size=train_size)
        return x_train , x_test , y_train , y_test

    @staticmethod
    def pca(x_train , x_test  , path , fileName: str = "PCA_model.sav"  , Num_component = 15):
        """
        @TODO: fit PCA model on the x_train and transform x_train and x_test
        :param x_train: the part of the data that is used to train PCA model
        :param x_test: this part of the data is to be transformed and returned to be used in the ML models
        :param path: if train is true then path is the path where we should save the model otherwise
                     it will be the path that we can find the pretrained pca_model in.
        :param fileName: file name to save the PCA model with
        :param Num_component: is used to specify the number of principal components to keep
        :return:
        """

        pca = PCA(n_components=Num_component)
        pca.fit(x_train)
        pickle.dump(pca, open(path+fileName, 'wb'))
        x_train = pd.DataFrame(pca.transform(x_train))
        x_test = pd.DataFrame(pca.transform(x_test))
        return x_train, x_test

    @staticmethod
    def expect_pca(x, path , fileName: str = "PCA_model.sav"):
        """
        @TODO: fit PCA model on the x_train and transform x_train and x_test
        :param x: the data that needs to be transformed via the PCA model.
        :param path: the path where the model exists.
        :param fileName: the name of the file that contains the desired model.
        :return: transformed form of the input data.
        """
        pca = pickle.load(open(path + fileName, 'rb'))
        x = pd.DataFrame(pca.transform(x))
        return x