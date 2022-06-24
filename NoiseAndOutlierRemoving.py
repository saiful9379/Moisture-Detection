'''
@ Discriptiton : this script use for noise and outlier removing purposes from raw data
@ Author       : Saiful Islam
@ Co-Author    : Rahat, Himel, Payal 
@ Copyright    : tau-research
@ License      : MIT
'''

import os
import numpy as np
import pandas as pd
from termcolor import colored
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess


DEBUG = True
LOWESS_FRACTION_THRESHOLD = 0.05

# filtered = lowess(measurements, input_range, frac=0.05)
def get_read_csv(file_path):
    '''
    Args:
        this function use for csv data reading
        input:
            file_path {str} - input data file path
        return:
            data {numpy} - moisture reading
    '''
    #read csv data
    data = pd.read_csv (file_path)
    return data

def get_save_logs(data,filtered,file_name="Unknow",log_dir="logs"):
    '''
    Args:
        this function use for data visualization and save
        input:
            data       {numpy}  - moisture data
            filtered   {numpy}  - after removing moisture and outlier data
            file_name  {str}    - input file name
            log_dir    {str}    - log save dir
        return:
            None
    '''
    time = data.time
    value = data.V
    plt.figure(figsize=(20,12))
    plt.title('Moisture Raw and Filter data curve')
    plt.plot(time, value, label = "line_1:raw data")
    plt.plot(filtered[:, 0],filtered[:, 1], 'r-', label = "line_2:filter data")
    plt.xlabel('x - axis(Time)')
    # Set the y axis label of the current axis.
    plt.ylabel('y - axis (Value)')
    # Set a title of the current axes.
    # Display a figure.
    # plt.show()
    plt.legend(loc='best')
    save_dir = os.path.join(log_dir,file_name+"_remove_noise_and_outlier.png")
    plt.savefig(save_dir)
    # print("================================================")
    


def removing_noise_and_outlier(data, LOWESS_FRACTION_THRESHOLD, file_name="Unknown",log_dir="logs",DEBUG = False):
    print(colored(' ✔ Process 1 ', 'green'))
    if isinstance(data, str):
        data = get_read_csv(file_path)
    else:
        data = data

    time = data.time
    value = data.V
    print("  ⮩ Noise and Outlier Removing...: ",end='',flush=True)
    filtered = lowess(value,time, frac=LOWESS_FRACTION_THRESHOLD)
    print(colored('Done', 'green'))
    if DEBUG:
        print("  ⮩ Noise and Outlier Removing Figure Save...: ",end='',flush=True)
        get_save_logs(data,filtered,file_name=file_name,log_dir=log_dir)
        print(colored('Done', 'green'),"\n")
    # print(filtered)
    return filtered

if __name__ == "__main__":
    file_path = "/home/saiful/Desktop/moisture_detection/MOI_D_V1.0.0/data/Csv-format data/dat_9_noise+outliar.csv"
    # data = get_read_csv(file_path)
    file_name = os.path.basename(file_path)[:-4]
    removing_noise_and_outlier(file_path,LOWESS_FRACTION_THRESHOLD,file_name = file_name,log_dir="logs",DEBUG=DEBUG)