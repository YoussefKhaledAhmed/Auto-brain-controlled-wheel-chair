"""
 File name: Data_Prepare.
 Date: 16/2/2023
 Author: Youssef Khaled Ahmed
 Description: this file is responsible for getting the required data from a specific path
              and then preparing it.
"""

"""
 imported files and libraries:
  pandas: to deal with DataFrames.
  Files_manager: to get the required data from the passed path.
"""
import math
import pandas as pd
from PreProcessing.Files_manager import FilesManager

"""
 class: DataPrepare
 Attributes: none.
 Methods: 
    init: for initializing the class -once an object from this class is initialized- by
          making an object from the class FilesManager.
    get_Data: getting the csv data from the passed path.
    get_DataFromFiles: getting the data from a group of files that their paths are passed.
    concatData: concatenating data that is passed as a list and making it a single DataFrame.
    concatFreq: concatenating data according to the passed frequency.
    concatFrequencies: concatenating data according to the passed frequencies not a single one.
    extractTrials: extracting trials from the passed data according to the number of seconds the 
                   single trial takes.
"""
class DataPrepare:
    def __init__(self):
        """
        @TODO initializing manager as an object from the class FilesManager
        """
        self.manager = FilesManager

    def get_Data(self , filePath: str):
        """
        @TODO: getting data from the passed path
        :param filePath: the path where the file exists
        :return: data as DataFrame
        """
        return self.manager.getData(filePath)

    def get_DataFromFiles(self , paths: list , concat = False):
        """
        @TODO: it takes the paths as a list then it loops on that list after that it
               returns the  data present in this list in the form of list of DataFrame
        :param paths: list of strings
        :param concat: if True it will concatenate the data otherwise it won't
        :return: data present in all files as a list of DataFrame
        """
        # checking if the passed argument if from 'list' type.
        if not isinstance(paths , list):
            raise Exception("the paths are not passed as a 'list'.")
        data = list()
        for path in paths:
            data.append(self.get_Data(path))
        # if concat is True it will call "concatData" which is responsible for concatenating the data.
        if concat:
            data = self.concatData(data)
        return data

    @staticmethod
    def concatData(list_of_data : list):
        """
        @TODO: this function is responsible for concatenating data from the files
               that exist in the passed pass.
        :param list_of_data: list of DataFrames
        :return: concatenated data in the form of on DataFrame
        """
        # checking if the passes argument is of type 'list'.
        if not isinstance(list_of_data , list):
            raise AttributeError
        # checking if the elements of the list are 'DataFrame'.
        if not isinstance(list_of_data[0] , pd.DataFrame):
            raise AttributeError
        return pd.concat(list_of_data , axis = 0 , ignore_index = True)

    @staticmethod
    def concatFreq(Data: pd.DataFrame , freq , labelName = 'Label'):
        """
        @TODO: this function concatenates the data with the passed frequency but single freq.
        :param Data: the data which contains that with the required frequency.
        :param freq: the required frequency.
        :param labelName: it is the name of the column that contains the frequencies.
        :return: DataFrame with the required frequency.
        """
        # checking on the type of the Data that is passed
        if not isinstance(Data , pd.DataFrame):
            raise AttributeError
        # checking on the type of the required frequency
        if not isinstance(freq , int) and not isinstance(freq , float) and not isinstance(freq , str):
            raise AttributeError
        # checking on the type of the name of the column that contains the frequencies (i.e., Label)
        if not isinstance(labelName , str):
            raise AttributeError
        return Data[Data[labelName] == float(freq)]

    def concatFrequencies(self , Data: pd.DataFrame , frequencies: list , labelName: str  = 'Label'):
        """
        @TODO: this function is responsible for concatenating frequencies not a single frequency.
               this function isn't "@staticmethod" because it will use some methods of the class.
        :param Data: the whole data that contains the required frequency.
        :param frequencies: it is a list of the required frequencies.
        :param labelName: it is the name of the column that contains the frequencies.
        :return: DataFrame with the required frequencies.
        """
        # checking the type of the passed data.
        if not isinstance(Data , pd.DataFrame ):
            raise AttributeError
        # checking the type of the passed frequencies if they are list or not.
        if not isinstance(frequencies , list):
            raise AttributeError
        # checking the type of the first element of the frequency list.
        if not isinstance(frequencies[0] , int) and not isinstance(frequencies[0] , float) \
                and not isinstance(frequencies[0] , str):
            raise AttributeError
        # checking on the type of the name of the column that contains the frequencies (i.e., Label).
        if not isinstance(labelName , str):
            raise AttributeError
        # data is a variable of type 'list' that will contain the data of the required frequencies.
        # data will be list of DataFrames.
        data = list()
        # looping on the frequencies and appending the data each frequency in a list
        for freq in frequencies:
            data.append(self.concatFreq(Data , freq))
        # this function will return the output of the function "concatData" that will take the
        # list of the DataFrames that we made using the previous for loop and concatenate it
        # to make on DataFrame that contains the data of the required frequencies concatenated.
        return self.concatData(data)

    @staticmethod
    def extractTrials(data: pd.DataFrame, numOfSecs , freq=128):
        """
        @TODO: this function takes data as DataFrame and divide it into trials
               depending on the number of seconds that the session takes and
               frequency as by multiplying them we will get the total number
               of rows that each trial or epoch has.
        :param data: the data as a whole DataFrame.
        :param numOfSecs: number of seconds that the recording of that data took.
        :param freq: frequency where the data recorded at.
        :return: it returns the same data but in the form of list this is done by slicing the data.
        """
        # checking the type of the data.
        if not isinstance(data , pd.DataFrame):
            raise AttributeError
        # checking the type of the "numOfSecs" variable.
        if not isinstance(numOfSecs , int):
            raise AttributeError
        # checking the type of the "freq" variable.
        if not isinstance(freq , int):
            raise AttributeError
        # trials is the list where the data is stored after slicing.
        trials = list()
        # step: is the number of steps that the loop should skip
        #       in a simpler way it's the number of data recorded in a single trial or epoch.
        #       so, we multiplied the frequency which is the number of data recorded in a single second
        #           and then multiply it by the total number of seconds that the trial took.
        step = freq * numOfSecs
        # data.shape will return a list of [number of rows , number of columns]
        # so we just need the number of rows so, data.shape[0] will get it.
        # then, the step of the for loop will be that we calculated before.
        # through the for loop we used iloc[] method to get the specific rows that
        # we need from the DataFrame.
        for i in range(0, data.shape[0], step):
            # i:(i + step), means rows from i to (i + step).
            # :, means that we need the whole columns and that's true.
            trials.append(data.iloc[i:(i + step), :])
        return trials

