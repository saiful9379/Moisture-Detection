'''
@ Discriptiton : this script use for darivative and peak value detection from noise and ourlier remove data
@ Author       : Saiful Islam
@ Co-Author    : Rahat, Himel, Payal 
@ Copyright    : tau-research
@ License      : MIT
'''
import os
import numpy as np 
import pandas as pd
from pycse import deriv
from termcolor import colored
import matplotlib.pyplot as plt
# from scipy.signal import find_peaks
from utility.ampd import find_peaks, find_peaks_original, find_peaks_adaptive

DEBUG = True
OUTPUT_DIR = "logs"
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
    data = pd.read_csv(file_path)
    return data

def get_save_data_fig(time,value,derivative_data,file_name="Unknown",log_dir="logs"):
    plt.figure(figsize = (15,6))
    plt.title('Moisture Raw and 1st derivative data curve')
    plt.plot(time,value,label='Raw Data')
    plt.plot(time, derivative_data,'r-',label='1st derivative')
    plt.xlabel('x - axis(Time)')
    # Set the y axis label of the current axis.
    plt.ylabel('y - axis (Value)')
    plt.legend(loc='best')
    fig_file_name = os.path.join(log_dir,file_name+"_derivative.png")
    plt.savefig(fig_file_name)
    # plt.show()

def get_save_peak_fig(time,data,derivative_data,peaks,file_dir="Unknown"):
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(time, derivative_data,lw=4)
    plt.plot(time, data, 'gs', label='raw data')
    plt.plot(time[peaks], derivative_data[peaks], 'rs', label='Peak value')
    plt.legend()
    ax.set_xlabel('Time [s]',fontsize=14)
    ax.set_ylabel('value',fontsize=14)
    ax.set_title('Experiment 1',fontsize=14)
    plt.savefig(file_dir)

def get_save_isolation_cycle_fig(org_and_isolation_cycle_data,file_name_dir="Unknown"):
    time,value,cycle_time,cycle_data = org_and_isolation_cycle_data
    plt.figure(figsize = (15,6))
    plt.title('Moisture Raw and 1st derivative data curve')
    plt.plot(time,value,label='Raw Data')
    plt.plot(cycle_time, cycle_data,'r-',label='isolation curve')
    plt.xlabel('x - axis(Time)')
    # Set the y axis label of the current axis.
    plt.ylabel('y - axis (Value)')
    plt.savefig(file_name_dir)


def get_pick_value(time,data,derivative_data,file_name="Unknown",log_dir="logs",DEBUG=False):

    peaks= find_peaks(derivative_data)
    print(colored('Done', 'green'))
    
    # print(peaks)
    if DEBUG:
        peak_file_name = os.path.join(log_dir,file_name+"_peak_detection.png")
       
        print("  ⮩ Peak Figure Saving ... : ", end='',flush=True)
        get_save_peak_fig(time,data,derivative_data,peaks,file_dir=peak_file_name)
        print(colored('Done', 'green'))
        file_log_dir = os.path.join(log_dir,file_name)
        os.makedirs(file_log_dir,exist_ok= True)
        cnt = 0
       
        for x in range(0,len(peaks)-1): 
            # plt.figure(figsize=(10, 5))
            print("    ⮩ Cycle Saving {} ... : ".format(cnt),  end='',flush=True)
            cycle_file_name_dir = os.path.join(file_log_dir,file_name+"_cycle_"+str(cnt)+".png")
            cycle_time=time[peaks[x]:peaks[x+1]]
            cycle_data=data[peaks[x]:peaks[x+1]]
            orginal_and_cycle_issolation_data = [time,data,cycle_time,cycle_data]
            get_save_isolation_cycle_fig(orginal_and_cycle_issolation_data,file_name_dir=cycle_file_name_dir)
            print(colored('Done', 'green'))
            cnt+=1
            
            
            # plt.plot(time1,data1)

    return peaks

def get_derivative(data,file_name="Unknown",log_dir="logs",DEBUG = False):

    print(colored(' ✔ Process 2 ', 'green'))

    if isinstance(data,str):
        data = get_read_csv(file_path)
        time = data.time
        data = data.V
    else:
        filter_data = data
        time = filter_data[:, 0]
        data = filter_data[:, 1]

    derivative_data = deriv(time,data)
     
    print(colored('  ⮩ Data Derivative... : '),end='', flush=True)
    # time.sleep(1)
    if DEBUG:
        get_save_data_fig(time,data,derivative_data,file_name=file_name,log_dir=log_dir)
    print(colored('Done', 'green'),"\n")

    print(colored(' ✔ Process 3 ', 'green'))
    print('  ⮩ Getting Peak Point... : ',end='',flush=True)
    
    peaks = get_pick_value(time,data,derivative_data,file_name=file_name,log_dir=log_dir,DEBUG=DEBUG)

    return peaks,derivative_data



if __name__ == "__main__":
    file_path = "/home/saiful/Desktop/moisture_detection/MOI_D_V1.0.0/data/Csv-format data/interpolated_dat_6.csv"
    file_name = os.path.basename(file_path)[:-4]
    peaks, derivative_data = get_derivative(file_path,file_name=file_name,log_dir=OUTPUT_DIR,DEBUG = DEBUG )