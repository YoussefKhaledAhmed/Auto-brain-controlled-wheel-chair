import matplotlib.pyplot as plt
import numpy as np
import math


channelDef = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
# matplotlib.use('Qt5Agg')
class graphs:
    @staticmethod
    def TIME_visualizationOfAllElectrodes(data ,title: str, channels_def = channelDef):
        """
        @TODO: it takes one trial(epoch) of the data and plot it.
        :param: data: just one trial(epoch) of the data.
        :param: title: the title that should be put over the plot
        :return: void (i.e. doesn't return anything).
        """
        #@TODO: 1. drop the column that has the name "Label"
        #       2. plot the data in the time domain

    # 1. this line drops the "Label" column
        data = data.drop(columns = data.columns[-1])
    # 2. plotting the data with figure size 10 width and 7 height
        plt.figure(figsize = (10,7))
        # by adding "80*(np.arange(13,-1,-1))" to the data we have
        # we make sure that the data of each electrode will appear separate
        # as if we don't add this part they will all appear in a single line
        # over each other and will be hard to see the data of specific electrode
        plt.plot(data + 80*(np.arange(13,-1,-1)))
        plt.xlabel("time in secs")
        plt.ylabel("amplitude")
        plt.title("EEG signal in time domain ( " + title +" )")
        plt.legend(channels_def)
        plt.show()

    @staticmethod
    def TIME_visualizationOfEachElectrode(data , channels_def):
        """
        @TODO: it takes one trial(epoch) of the data and plot each electrode alone.
        :param data: just one trial(epoch) of the data.
        :param channels_def: it is a list contains the names of the channels.
        :return: void (i.e. doesn't return anything).
        """
        data = data.drop(columns = data.columns[-1])
        fig , axis = plt.subplots(len(channels_def) , 1 , figsize = (20 , 100))
        for i,channel in enumerate(channels_def):
            axis[i].plot(data.iloc[: , i])
            axis[i].set_title(channel)
        plt.subplots_adjust(hspace = 1)
        plt.show()


    @staticmethod
    def TIME_visualizationOfSpecificElectrodes(data , electrode):
        if not isinstance(electrode , list):
            raise Exception("electrode isn't of list type")
        if len(electrode) == 1:
            plt.figure(figsize=(10, 7))
            plt.plot(data[electrode[0]])
            plt.title(electrode[0])
            plt.show()
        else:
            data = data.drop(columns= data.columns[-1])
            fig, axis = plt.subplots(len(electrode), 1, figsize=(20, 100))
            for i, channel in enumerate(electrode):
                axis[i].plot(data[channel])
                axis[i].set_title(channel)
            plt.subplots_adjust(hspace=1)
            plt.show()

    @staticmethod
    def closeGraphs():
        plt.close('all')


    @staticmethod
    def FREQ_ofAllChannels():
        pass

    @staticmethod
    def FREQ_ofSpecificChannels(freq , power_or_ampl , label = -1 , channels:list = channelDef):
        def_freq = [7.5, 8.57, 10, 12]
        # colors for the lines
        colors = ['g', 'r', 'b', 'y']
        num_channels = len(channels)
        if num_channels > 7:
            half = math.ceil(num_channels / 2)
            fig , axis = plt.subplots(half , 2 , figsize = (20 , 20))
            for i , curr_ch in enumerate(channels):
                f = freq[i]
                Pxx_den = power_or_ampl[i]
                for xc , color in zip(def_freq , colors):
                    axis[i % half , int(i >= half)].axvline(x = xc , c = color)
                axis[i % half , int(i >= half)].plot(f , Pxx_den)
                axis[i % half , int(i >= half)].set_title(curr_ch)
                axis[i % half , int(i >= half)].grid()
        else:
            fig, axis = plt.subplots(num_channels , figsize=(20, 20))
            for i, curr_ch in enumerate(channels):
                f_P_i = channelDef.index(channels[i])
                f = freq[f_P_i]
                Pxx_den = power_or_ampl[f_P_i]
                for xc, color in zip(def_freq, colors):
                    axis[i].axvline(x=xc, c=color)
                axis[i].plot(f, Pxx_den)
                axis[i].set_title(curr_ch)
                axis[i].grid()
        if label != -1:
            fig.suptitle("frequency: {}".format(label))
        plt.show()






    # @staticmethod
    # def welch_vis(freq, power, lable, channel):
    #     """
    #         used to visualize power spectrum for each given channel
    #         Parameters:
    #             freq,power: output from welch function "freq-power"
    #             channel: list of channel to visualize
    #             lable: list of frequecnies
    #     """
    #     channels_def = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
    #     num_channels = len(channel)
    #     xcoords = [7.5, 8.57, 10, 12, 6.66, 15]
    #     # colors for the lines
    #     colors = ['g', 'r', 'b', 'r', 'y', 'b']
    #
    #     if num_channels > 7:
    #         half = math.ceil(num_channels / 2)
    #         ig, axis = plt.subplots(half, 2, figsize=(20, 20))
    #         for i, current_c in enumerate(channel):
    #             # to print till freq approx equals 50 hz
    #             f = freq[current_c][:-80]
    #             Pxx_den = power[current_c][:-80]
    #             for xc, c in zip(xcoords, colors):
    #                 axis[i % half, int(i >= half)].axvline(x=xc, label='line at x = {}'.format(xc), c=c)
    #             axis[i % half, int(i >= half)].plot(f, Pxx_den)
    #             axis[i % half, int(i >= half)].set_title(channels_def[current_c])
    #             axis[i % half, int(i >= half)].grid(True)
    #     else:
    #         ig, axis = plt.subplots(num_channels, figsize=(20, 20))
    #         for i, current_c in enumerate(channel):
    #             # to print till freq approx equals 50 hz
    #             f = freq[current_c][:-80]
    #             Pxx_den = power[current_c][:-80]
    #             for xc, c in zip(xcoords, colors):
    #                 axis[i].axvline(x=xc, label='line at x = {}'.format(xc), c=c)
    #             axis[i].plot(f, Pxx_den)
    #             axis[i].set_title(channels_def[current_c])
    #             axis[i].grid(True)
    #
    #     ig.suptitle('frequency:{}'.format(lable))
    #
    #     plt.title
    #     plt.show()


if __name__ == "__main__":
    import pandas as pd
    import csv
    import numpy as np

    df = pd.read_csv(
        'D:/Graduation Project/Our graduation project/1. Project_of previous year/Our Project/EEG-SSVEP-DataSet/5_S/Test Data Kholy/U0000gi.csv')
    trials = list()
    for j in range(0, df.shape[0], 128 * 50):
        # trials.append(Data.iloc[i:i + 128 * Num_sec, :-1])
        trials.append(df.iloc[j:j + 128 * 50, :])
    channel_def = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
    graph = graphs
    graph.TIME_visualizationOfEachElectrode(trials[0], channel_def)
    graph.TIME_visualizationOfAllElectrodes(trials[0], channel_def)
    graph.TIME_visualizationOfSpecificElectrodes(trials[0], ['AF3', 'F7', 'F3'])




