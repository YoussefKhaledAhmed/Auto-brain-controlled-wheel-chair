from Manual_Process import mainProcess

if __name__ == "__main__":
    fileName = "trial_8_7_2023.csv"
    filePath = "D:/Graduation Project/Our graduation project/1. Project_of previous year/Our Project/Our Project/EEG-SSVEP-DataSet/5_S/Data/Youssef_8_7_2023/"
    pcaPath = "D:/Graduation Project/Brain-controlled-wheelchair-with-self-driving-mode/PCA_models/"
    MlModelsPath = "D:/Graduation Project/Brain-controlled-wheelchair-with-self-driving-mode/trained_MLModels/"
    MlUserName = "trial20-5"
    prediction = mainProcess(5, fileName, filePath, pcaPath, MlModelsPath, MlUserName)
    print("manual_predictions -> ", prediction)