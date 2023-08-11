from Recording.main import Collect, save
import sys

def record(record_t, record_label , fileName:str = "trial" , path:str = "D:/Graduation Project/Brain-controlled-wheelchair-with-self-driving-mode/recorded_Data/Train"):
    if not isinstance(record_t, int):
        record_t = int(record_t)
    collect = Collect(False)
    Data = collect.record(record_t)
    save(path + '/' + fileName
        ,
        Data, record_label)
    #print(Data.head())
    return Data

if __name__ == "__main__":
    t = int(sys.argv[1])
    label = int(sys.argv[2])
    name = sys.argv[3]
    trainPath = sys.argv[4]
    record(t , label , name , trainPath)
    # print("here")
