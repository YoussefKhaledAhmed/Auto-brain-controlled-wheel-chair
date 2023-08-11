import time
from PreProcessing.Data_Prepare import DataPrepare
from MainProcesses import liveProcess,offlineProcess,mainProcess
import sys
import serial
import glob

port = "COM7"  # The serial port of the Bluetooth module
baudrate = 9600  # The baud rate of the Bluetooth module

class AutoProcess:
    @staticmethod
    def live_process(t_Auto , fileName_live , filePath_live , pca_name_live ,
                       pca_path_live , ML_models_path_live , ML_userName_live):
        """
        @TODO:
        :param t_Auto: time to record
        :param fileName_live: fileName to save this data
        :param filePath_live: the path where the file exists
        :param pca_name_live:
        :param pca_path_live:
        :param ML_models_path_live
        :param ML_userName_live
        :return: prediction of the label
        """
        prediction_manual = liveProcess(real_time= t_Auto , file_name= fileName_live , file_path= filePath_live ,
                                      pca_name = pca_name_live, pca_path= pca_path_live , ML_models_path= ML_models_path_live ,
                                      ML_name= ML_userName_live)
        return prediction_manual

    @staticmethod
    def offline_process(data ,pca_name_offline ,
                       pca_path_offline , ML_models_path_offline , ML_userName_offline):
        """
        @TODO:
        :param data:
        :param pca_name_offline:
        :param pca_path_offline:
        :param ML_models_path_offline
        :param ML_userName_offline
        :return: prediction of the label
        """
        prediction_manual = offlineProcess(data= data,pca_name = pca_name_offline,
                                             pca_path=pca_path_offline, ML_models_path=ML_models_path_offline,
                                             ML_name=ML_userName_offline)
        return prediction_manual

    @staticmethod
    def prepareDataForOffline(t_offline , fileName_offline , filePath_offline):
        """
        @TODO:
        :param t_offline:
        :param fileName_offline:
        :param filePath_offline:
        :return:
        """
        process_ = mainProcess()
        prepare = DataPrepare()
        if isinstance(filePath_offline , list):
            realTime_data = prepare.get_DataFromFiles(glob.glob(filePath_offline), concat = True)
            offlineData = prepare.extractTrials(realTime_data, t_offline)
        else:
            realTime_data = process_.getRealTimeData(fileName=fileName_offline, path=filePath_offline)
            offlineData = prepare.extractTrials(realTime_data, t_offline)
        return offlineData

    @staticmethod
    def bluetoothSend(command):
        """
        @TODO:
        :param command:
        :return: void
        """
        command = str(command)
        print("send ", command, " to the motors")

        # Open the serial port
        ser = serial.Serial(port, baudrate)
        ser.write(command.encode())
        ser.close()

    @staticmethod
    def writeToTxtFile(command , Auto_txt_fileName):
        """
        @TODO:
        :param command:
        :param Auto_txt_fileName:
        :return:
        """
        with open(Auto_txt_fileName, "w") as file:
            file.truncate(0)
            file.write(command)



if __name__ == "__main__":
    print("\n\nAuto_mode activated:\n")
    t = int(sys.argv[1])
    fileName = sys.argv[2]
    filePath = sys.argv[3]
    pcaName = sys.argv[4]
    pcaPath = sys.argv[5]
    MlModelsPath = sys.argv[6]
    MlName = sys.argv[7]

    process = AutoProcess()
    liveFlag = False
    if liveFlag:
        print("live session starts:\n")
        while 1:
            live_prediction = process.live_process(t, fileName, filePath , pcaName , pcaPath, MlModelsPath, MlName)
            process.bluetoothSend(live_prediction)
            txt_filePath = "D:/Graduation Project/Brain-controlled-wheelchair-with-self-driving-mode/txt_file"
            txt_fileName = "txtFile.txt"
            process.writeToTxtFile(str(live_prediction) , txt_filePath+'/'+txt_fileName)
    else:
        print("offline session starts:\n")
        realTime_data_list = process.prepareDataForOffline(t , fileName , filePath)
        for x in realTime_data_list:
            time.sleep(1)
            offline_prediction = offlineProcess(x , pcaName , pcaPath, MlModelsPath, MlName)
            process.bluetoothSend(offline_prediction)
            txt_filePath = "D:/Graduation Project/Brain-controlled-wheelchair-with-self-driving-mode/txt_file"
            txt_fileName = "txtFile.txt"
            process.writeToTxtFile(str(offline_prediction), txt_filePath + '/' + txt_fileName)