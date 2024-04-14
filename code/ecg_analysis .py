import neurokit2 as nk
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def ecg_analysis(ecg):
    #Clean data
    ecg_cleaned = nk.ecg_clean(ecg, sampling_rate=1000)     #sampling_rate(採樣率)會依各台儀器的設定而有所不同
    
    #Find peaks
    peaks, info = nk.ecg_peaks(ecg_cleaned, sampling_rate=1000)
    
    #Calculate heart rate
    rpeaks = info["ECG_R_Peaks"]
    heartRate = nk.ecg_rate(rpeaks, sampling_rate=1000, desired_length=len(ecg_cleaned))    #利用r peaks來計算心率
    avg_heartRate = np.round(np.mean(heartRate), 5)     #計算平均心率(取至小數點下第五位)
    #print(avg_heartRate)
    
    '''
    #Non-Linear Domain Analysis
    hrv_nonlinear = nk.hrv_nonlinear(peaks, sampling_rate=1000, show=True)
    print(hrv_nonlinear)
    
    # Time-Domain Analysis
    hrv_time = nk.hrv_time(peaks, sampling_rate=1000, show=True)
    print(hrv_time)
    
    # Frequency-Domain Analysis
    hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000, show=True, normalize=True)
    print(hrv_freq)
   '''
    
    # All domain
    hrv_indices = nk.hrv(peaks, sampling_rate=1000, show=False)
    #print(hrv_indices)
    
    return avg_heartRate, hrv_indices

def standardize(data):
    object = StandardScaler()
    data = pd.DataFrame(object.fit_transform(data), columns=data.columns)
    return data
    

# main function

#建立儲存資料的dataframe和list
result = pd.DataFrame()
avg_heart = pd.DataFrame()
hrv = pd.DataFrame()
time = []

data = pd.read_csv("../OpenSignals_files/20231227/2023-12-27_21-11-03(converted).csv")

for i in range(0, 600000, 150000):    #range(開始的時間戳記, 結束的時間戳記, 移動的時間間隔)
    print("---------------------[", i ,"]---------------------")
    time.append(i)  #紀錄開始的時間戳記
    ecg = data['ecg'][i:i+300000]   #+300000:每次以300秒(5分鐘)作為一個window)
    avg_heartRate, hrv_indices = ecg_analysis(ecg)
    
    #合併資料成一個dataframe
    avg_heart =  pd.concat([avg_heart, pd.DataFrame([avg_heartRate]).T], ignore_index=True)
    hrv = pd.concat([hrv, hrv_indices], ignore_index=True)
    result = pd.concat([avg_heart, hrv],axis=1)
    result = result.rename(columns={0:'heart_avg'})
    print(result)
    
#standardization
result = standardize(result)

#加上時間戳記
result = pd.concat([pd.DataFrame([time]).T, result], axis=1)
result = result.rename(columns={0:'time_index'})

#顯示最後結果
print('\n最後結果:\n' ,result)
#儲存成另一csv檔
result.to_csv("../OpenSignals_files/20231227/analysis/2023-12-27_21-11-03(ecg_analysis).csv")



