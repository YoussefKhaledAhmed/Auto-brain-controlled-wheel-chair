import time
from PreProcessing.Data_Prepare import DataPrepare
from MainProcesses import liveProcess,offlineProcess,mainProcess
import sys
import serial
import glob

# port = "COM5"  # The serial port of the Bluetooth module
# baudrate = 9600  # The baud rate of the Bluetooth module

class ManualProcess:
    @staticmethod
    def live_process(t_manual , fileName_live , filePath_live , pca_name_live ,
                       pca_path_live , ML_models_path_live , ML_name_live):
        """
        @TODO:
        :param t_manual: time to record
        :param fileName_live: fileName to save this data
        :param filePath_live: the path where the file exists
        :param pca_name_live:
        :param pca_path_live:
        :param ML_models_path_live
        :param ML_name_live
        :return: prediction of the label
        """
        prediction_manual = liveProcess(real_time= t_manual , file_name= fileName_live , file_path= filePath_live ,
                                      pca_name = pca_name_live, pca_path= pca_path_live , ML_models_path= ML_models_path_live ,
                                      ML_name= ML_name_live)
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
        # command = str(command)
        # command = "0"
        print("send ", command, " to the motors")
        # # Open the serial port
        # ser = serial.Serial(port, baudrate)
        # ser.write(command.encode())
        # ser.close()
        # import time

        # import serial

        port = "COM7"  # The serial port of the Bluetooth module
        baudrate = 9600  # The baud rate of the Bluetooth module

        # Open the serial port
        ser = serial.Serial(port, baudrate)

        # Send some data to the Bluetooth module
        data1 = ["0", "1", "2", "3"]
        data = str(command)
        # print("type of data1[0] -> ",type(data1[0]))
        # print("type of data -> ",type(data))
        ser.write(data.encode())

        time.sleep(1)
        # print("before the for loop:\n")
        for i in range(0, 1):
            time.sleep(1)
            ser.write(data.encode())
            # print("data -> ", data)


        # Close the serial port
        # ser.close()


    @staticmethod
    def writeToTxtFile(command , txt_fileName_local):
        """
        @TODO:
        :param command:
        :param txt_fileName_local:
        :return:
        """
        with open(txt_fileName_local, "w") as file:
            file.truncate(0)
            file.write(command)



if __name__ == "__main__":
    print("\n\nManual_BCI_mode activated:\n")
    t = int(sys.argv[1])
    fileName = sys.argv[2]
    filePath = sys.argv[3]
    pcaName = sys.argv[4]
    pcaPath = sys.argv[5]
    MlModelsPath = sys.argv[6]
    MlName = sys.argv[7]
    process = ManualProcess()
    liveFlag = True
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
            time.sleep(2)
            offline_prediction = offlineProcess(x , pcaName , pcaPath, MlModelsPath, MlName)
            process.bluetoothSend(offline_prediction)
            txt_filePath = "D:/Graduation Project/Brain-controlled-wheelchair-with-self-driving-mode/txt_file"
            txt_fileName = "txtFile.txt"
            process.writeToTxtFile(str(offline_prediction), txt_filePath + '/' + txt_fileName)