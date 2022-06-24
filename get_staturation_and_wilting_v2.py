import os
import json
import numpy as np 
import pandas as pd
from termcolor import colored
from matplotlib import pyplot as plt
from pycse import deriv

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


def saturation_wilting_value(df_data,derivative,peaks,filename,DEBUG=False, log_dir="logs"):
    
    # if isinstance(data, ar)
    dCdt_numeric=derivative
    time =df_data.time
    data = df_data.V


    #from statsmodels.nonparametric.smoothers_lowess import lowess
    #filtered = lowess(measurements, input_range, frac=0.03)
    #pks, LSM, adaptive_scale = find_peaks_adaptive(filtered[:, 1], window=1000, debug=True)
    #pks, LSM, adaptive_scale = find_peaks_adaptive(dCdt_numeric, window=1000, debug=True)
    peaks= peaks
    allsat=[]
    allwilt=[]
    saturation=[]
    wilting=[]
    counters=0
    counterw=0
    satcounter=0
    wiltcounter=0
    
    sat_wilt_data = {}
    sat_wilt_data['device_id']=123445
    sat_wilt_data['Number_of_saturation']=0
    sat_wilt_data['Number_of_wilting']=0
    sat_wilt_data['Saturation'] = []
    sat_wilt_data['Wilting'] = []
    
    for x in range(len(dCdt_numeric)):

        if dCdt_numeric[x]>=0 and dCdt_numeric[x]<=1 and counterw==0:
            counters+=1
            saturation.append(x)

            continue

        else :
            if counters>10:
                allsat=np.append(allsat,saturation)
                satcounter+=1
                
                sat_wilt_data['Saturation'].append({  'cycle': satcounter, 'data': saturation})
                
            counters=0
            saturation=[]



        if dCdt_numeric[x]>=-1 and dCdt_numeric[x]<=0 and counters==0:
            counterw+=1
            wilting.append(x)


        else :
            if counterw>10 and counters==0:
                allwilt=np.append(allwilt,wilting)
                
                wiltcounter+=1
                sat_wilt_data['Wilting'].append({  'cycle': wiltcounter, 'data': wilting})
            counterw=0
            wilting=[]

        if x==len(dCdt_numeric)-1:

                if counters>10:
                    allsat=np.append(allsat,saturation)
                if counterw>10:
                    allwilt=np.append(allwilt,wilting)
                    
    sat_wilt_data['Number_of_saturation']=satcounter
    sat_wilt_data['Number_of_wilting']=wiltcounter
    
    # print("data : ",data)
    # print("time:",time)
    storejson={"device_id":sat_wilt_data}
    # print("all saturetion : ",allsat)
    if DEBUG:
        fig, ax = plt.subplots(figsize=(15,5))
        ax.plot(time, dCdt_numeric,lw=4)
        #filter data
        plt.plot(time,data)
        #derivative peak detection
        plt.plot(time[peaks], dCdt_numeric[peaks], 'rs', label='peaks')

        #predicted point
        # time = pd.DataFrame(time)
        # data = pd.DataFrame(data)

        plt.plot(time[allsat],data[allsat],'ko', label='Saturation point')
        plt.plot(time[allwilt],data[allwilt],'rs', label='Wilting point')
        plt.legend()
        ax.set_xlabel('Time [s]',fontsize=14)
        ax.set_ylabel('value',fontsize=14)
        ax.set_title('Experiment on Saturation and wilting point',fontsize=14)

        output_path = os.path.join(log_dir,filename+"_saturation_and_wilting_prediction.png")
        plt.savefig(output_path)

    return storejson        
        
        
def irregration_cycle_indentification(df_data,derivative, peaks,filename="unknown",log_dir="logs",DEBUG=False):
    print('  ⮩ Getting saturation and wilting Point... : ',end='',flush=True)
    storejson = saturation_wilting_value(df_data,derivative,peaks,filename,DEBUG,log_dir)
    print(colored('Done', 'green'),"\n")
if __name__ =="__main__":
    # for sample in range(1,11):
    # file_path = '/home/saiful/Desktop/moisture_detection/MOI_D_V1.0.0/data/Csv-format data/interpolated_dat_5.csv'
    file_path = "/home/saiful/Desktop/moisture_detection/MOI_D_V1.0.0/data/filter_data.csv"
    file_name = os.path.basename(file_path)
    df = pd.read_csv(file_path)
    df_data = df
    time = df.time
    data = df.V
    derivative_data = deriv(time,data)
    peaks= find_peaks(derivative_data)
    # plt.figure(figsize = (15,6))
    storejson = irregration_cycle_indentification(df_data,derivative_data,peaks,filename = file_name[:-4],log_dir=OUTPUT_DIR,DEBUG=DEBUG)
    