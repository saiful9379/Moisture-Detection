'''
@ Discriptiton : This is core function for moisture detection
@ Author       : Saiful Islam
@ Co-Author    : Rahat, Himel, Jhon 
@ Copyright    : tau-research
@ License      : MIT
'''
import os
import numpy as np
import pandas as pd
import csv
from termcolor import colored
import matplotlib.pyplot as plt
from NoiseAndOutlierRemoving import removing_noise_and_outlier
from Derivativte_and_Pick_value import get_derivative
from get_staturation_and_wilting_v2 import irregration_cycle_indentification
# DEBUG True to save all logs
DEBUG = True
# make sure your input data path
# DATA_PATH = "/home/saiful/Desktop/moisture_detection/MOI_D_V1.0.0/data/Csv-format data/dat_5_noise+outliar.csv"
DATA_PATH = "/home/saiful/Desktop/moisture_detection/MOI_D_V1.0.0/data/Csv-format data/interpolated_dat_5.csv"
OUTPUT_DIR = "logs"

#lowess function noise removing threshold
LOWESS_FRACTION_THRESHOLD = 0.05

# need interpulation if we want
def get_interpulation_data():
    pass

def get_csv_file_data(file_path):
    data = pd.read_csv (file_path)
    return data


def get_save_data_fig(time,value,file_name="unknown"):
    file_save_path_dir = os.path.join(OUTPUT_DIR,file_name+".png")

    plt.title('Moisture Raw data')
    plt.plot(time, value, label = "raw data")
    plt.xlabel('x - axis(Time)')
    # Set the y axis label of the current axis.
    plt.ylabel('y - axis (Value)')
    plt.savefig(file_save_path_dir)


def csv_generator(time,value):
    with open('logs/filter_data.csv', mode='w') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        employee_writer.writerow(['time', 'V'])
        for t,v in zip(time,value):
            employee_writer.writerow([str(t), str(v)])

def core_operation(file_path,DEBUG= False):
    
    print(colored(' ✔ ', 'green'),"Start Processing ....................")
    file_name = os.path.basename(file_path)
    print(colored(' ✔ ', 'green'),"Data Reading :",end='',flush=True)
    if isinstance(file_path,str):
        data = get_csv_file_data(file_path)
    else:
        data = file_path
    print(colored('Done', 'green'))
    # print(colored(' ✔ Process 1 ', 'green'))
    time = data.time
    value = data.V
    if DEBUG:
        print(colored(' ✔ ', 'green'),"Data Figure Saving :",end='',flush=True)
        get_save_data_fig(time,value,file_name=file_name)
        print(colored('Done', 'green'))

    filtered = removing_noise_and_outlier(data, LOWESS_FRACTION_THRESHOLD, file_name=file_name,log_dir = OUTPUT_DIR,DEBUG = DEBUG)
    peaks,derivative_data = get_derivative(filtered,file_name=file_name,log_dir = OUTPUT_DIR,DEBUG = DEBUG)
    print(colored(' ✔ Process 4 ', 'green'))
    tilter_time, filter_value = filtered[:, 0] ,filtered[:, 1]
    print(type(filtered))
    df_data = pd.DataFrame(filtered,columns=['time', 'V'])
    print(df_data)
    get_save_data_fig(tilter_time,filter_value,file_name[:-4]+"_filter_")
    csv_generator(tilter_time,filter_value)
    irregration_cycle_indentification(df_data,derivative_data, peaks,filename=file_name,DEBUG = DEBUG, log_dir = OUTPUT_DIR)
    # storejson = irregration_cycle_indentification(filtered,derivative_data,time,peaks,filename= file_name[:-4],DEBUG= DEBUG, log_dir= OUTPUT_DIR)


    print("\n",colored(' ✔ ', 'green'),"Process succefully :",colored('Done', 'green'),"\n")

if __name__ == "__main__":
    core_operation(DATA_PATH, DEBUG = DEBUG)
