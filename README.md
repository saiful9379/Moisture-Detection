## Moisture Detection 

Moisture detection project menual


## File Structure

```
MOI_D_V1.0.0
    ├── logs
    ├── prediction.py
    └── utility
        ├── ampd.py
        ├── Derivativte_and_Pick_value.py
        └── NoiseAndOutlierRemoving.py
```
## Requirememt
Please have a look requirement file or  given below,

```
matplotlib==3.1.2
numpy==1.19.5
pandas==1.1.5
pycse==2.0.4
scipy==1.5.4
```

## Testing

please make sure all requirement and run ```predict.py``` script. and also make sure input data path directory.

__N.B__: please check log directory all output save here.


### Raw data Figure
![Alt text](./logs/interpolated_dat_5.csv.png "Raw data Figure")

### Noise and Outlier removing Figure
![Alt text](./logs/interpolated_dat_5.csv_remove_noise_and_outlier.png  "Noise and Outlier removing Figure")

### Derivaive
![Alt text](./logs/interpolated_dat_5.csv_derivative.png  "Derivaive")


### Peak Value Detection
![Alt text](./logs/interpolated_dat_5.csv_peak_detection.png  "Derivaive")

### Saturation and wilting prediction
![Alt text](./logs/interpolated_dat_5.csv_saturation_and_wilting_prediction.png  "Derivaive")


### Cycle Isolation

![Alt text](./logs/interpolated_dat_5.csv/interpolated_dat_5.csv_cycle_0.png "Cycle Isolation ") 
![Alt text](./logs/interpolated_dat_5.csv/interpolated_dat_5.csv_cycle_1.png "Cycle Isolation ") 
![Alt text](./logs/interpolated_dat_5.csv/interpolated_dat_5.csv_cycle_2.png "Cycle Isolation ") 
![Alt text](./logs/interpolated_dat_5.csv/interpolated_dat_5.csv_cycle_3.png "Cycle Isolation ") 
![Alt text](./logs/interpolated_dat_5.csv/interpolated_dat_5.csv_cycle_4.png "Cycle Isolation ")

## Next Operation
Upcomming

# Contributor
Tau - TECH_TEAM



