import os
import pandas as pd

class FilesManager:
    @staticmethod
    def getData(filePath : str):
        """
        @TODO: get CSV data from the mentioned path
        :param filePath: the path were the needed file exists.
        :return: data as DataFrame
        """
        if not isinstance(filePath , str): # checking if the file path is from type 'string'.
            raise Exception("this path isn't from the type 'string'.")
        if not os.path.exists(filePath): # checking if this directory do exist.
            raise Exception("this file doesn't exist in this directory.")
        return pd.read_csv(filePath)

    @staticmethod
    def deleteFile(filePath: str):
        """
        @TODO: deleting the mentioned file from its directory through the passed path
        :param filePath: the path were the needed file exists.
        :return: void
        """
        if not isinstance(filePath , str): # checking if the file path is from type 'string'.
            raise Exception("this path isn't from the type 'string'.")

        if not os.path.exists(filePath):  # checking if this directory do exist.
            raise Exception("this file doesn't exist in this directory.")
        else:
            os.remove(filePath)
            print("File is deleted.")