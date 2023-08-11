# importing the calsses:
from PreProcessing.Data_Prepare import DataPrepare
from Processing.Filter import Filters
from Processing.analysis import staticSpectralAnalysis , multivariateComponentsAnalysis
from ML_models.Models import ML_models
from Recording.main import Collect, save
from PreProcessing.Files_manager import FilesManager
import numpy as np

#importing other libraries:
import os
import glob
import time
import sys
import pandas as pd

class mainProcess:
    @staticmethod
    def record(t, label, fileName: str = "trial",
               path: str = "D:/Graduation Project/Brain-controlled-wheelchair-with-self-driving-mode/recorded_Data/Real_time"):
        if not isinstance(t, int):
            t = int(t)
        collect = Collect(False)
        Data = collect.record(t)
        save(path + '/' + fileName
             ,
             Data, label)
        # print(Data.head())
        return Data
    @staticmethod
    def getRealTimeData(fileName , path):
        manager = DataPrepare()
        return manager.get_Data(path + '/' + fileName)

    @staticmethod
    def process(raw_data , pca_name , pca_path , ML_models_path , ML_name , time_of_single_trial: int = 5 , lowCut_filter:int = 5 , highCut_filter:int = 40 , visualize = False ,
                trial_num_to_visualize: int = 0):
        """
        @TODO: this function is responsible of processing the signal through 3 steps:
               1. applying CAR(Common Average Rejection).
               2. filtering the data: between 5, 40.
               3. applying welch to the filtered data to extract the required features as power and freq.
        :param raw_data: realTime_data
        :param pca_name:
        :param pca_path: path of the PCA model
        :param ML_models_path: path to the machine learning models
        :param ML_name: name of the user where the model is trained on his data
                            such that the full name will be: model_name + user_name
                            so, for example LogisticRegression_YoussefKhaled
                            where the "LogisticRegression_" is defined automatically
                            and same for other defined ML models in the Models.py file
        :param time_of_single_trial: time of the single trial in seconds
        :param lowCut_filter: low cut frequency to apply to the bandpass filter
        :param highCut_filter: high cut frequency to apply to the bandpass filter
        :param visualize: must be set to True to visualize: raw signal, CAR signal, Filtered signal, welch output.
        :param trial_num_to_visualize: what trial is needed to be visualized.
        :return: void
        """
        """
        1. making objects of the following classes
        """
        fltr = Filters()
        analysis = staticSpectralAnalysis()
        pca = multivariateComponentsAnalysis()
        ml_models = ML_models()

        """
        2. processing the data with 3 steps
        """
        #1. CAR:
        data_car = analysis.CAR(raw_data.copy())
        #2. filtering
        data_filter = fltr.butter_bandpassFilter(data_car.copy() , 5 , 40 , train = False)
        #3. welch method
        data_welch = analysis.welch(data_filter.copy() , timeOfOneEpoch = 1 , train = False)
        #4. Feature extraction
        data_features = analysis.featureExtraction_welch(data_welch, 3, ['O1', 'O2'],
                                                         train=False)
        # print("pca_path -> ",pca_path)
        # print("pca_name -> ",pca_name)
        data_PCA = pca.expect_pca(data_features, pca_path , fileName=pca_name)
        #if logistic regression
        # prediction = ml_models.expect_LogisticRegression_with_GridSearchCV(x=data_PCA, path=ML_models_path,userName=ML_userName)
        model = ml_models.load_MLModel(ML_models_path, ML_name)
        prediction = model.predict(data_PCA)
        # Get the predicted class labels
        predicted_class_labels_index = np.argmax(prediction, axis=0)
        prediction = prediction[predicted_class_labels_index]
        return prediction

    @staticmethod
    def delete_RealTime_data(fileName , path):
        manager = FilesManager()
        manager.deleteFile(path + '/' + fileName)




def liveProcess(real_time , file_name , file_path , pca_name , pca_path , ML_models_path , ML_name):
    """
    @TODO:
    :param real_time: time to record
    :param file_name: fileName to save this data
    :param file_path: the path where the file exists
    :param pca_name:
    :param pca_path:
    :param ML_models_path:
    :param ML_name:
    :return: prediction of the label
    """
    process = mainProcess()
    process.record(t = real_time , label = -1 , fileName = file_name , path = file_path)
    realTime_data = process.getRealTimeData(fileName = file_name , path = file_path)
    manual_prediction = process.process(realTime_data , pca_name=pca_name , pca_path=pca_path , ML_models_path=ML_models_path ,
                           ML_name=ML_name)
    process.delete_RealTime_data(fileName=file_name , path=file_path)
    return manual_prediction

def offlineProcess(data ,pca_name , pca_path , ML_models_path , ML_name):
    """
        @TODO:
        :param data:
        :param pca_name:
        :param pca_path:
        :param ML_models_path:
        :param ML_name:
        :return: prediction of the label
        """
    process = mainProcess()
    manual_prediction = process.process(data, pca_name=pca_name, pca_path=pca_path,
                                    ML_models_path=ML_models_path,
                                    ML_name=ML_name)
    return manual_prediction