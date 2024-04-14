import neurokit2 as nk
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
global glo_signals

def eda_analysis(eda):
    
    #處理raw data
    signals, info = nk.eda_process(eda, sampling_rate=1000)
    
    #提取清洗過後的eda數據
    cleaned = signals["EDA_Clean"]
    
    #計算各項數據
    signal_avg = np.mean(cleaned)                        #計算單位時間內eda signal的平均值
    signal_std = np.std(cleaned)                         #計算單位時間內eda signal的平均值
    amplitude_avg = np.nanmean(info["SCR_Amplitude"])    #計算單位時間內SCR(Phasic)signal各個波的震幅平均值
    avg_peak = len(info["SCR_Peaks"])/5                  #計算單位時間內SCR(Phasic)signal的波峰個數
    
    return signal_avg, signal_std, amplitude_avg, avg_peak


def standardize(data):
    object = StandardScaler()
    data = pd.DataFrame(object.fit_transform(data), columns=data.columns)
    return data



# main function
result = pd.DataFrame()
time = []

data = pd.read_csv("../OpenSignals_files/20231227/2023-12-27_20-55-13(converted).csv")

for i in range(0, 700000, 150000):
    print("---------------------[", i ,"]---------------------")
    time.append(i)  #紀錄開始的時間戳記
    eda = data['eda'][i:i+300000]   #+300000:每次以300秒(5分鐘)作為一個window)
    signal_avg, signal_std, amplitude_avg, avg_peak = eda_analysis(eda)
    
    #合併資料成一個dataframe
    result = pd.concat([result, pd.DataFrame([signal_avg, signal_std, amplitude_avg, avg_peak]).T], ignore_index=True)
    print(result)
  
#standardization
result = standardize(result)

#加上時間戳記
result = pd.concat([pd.DataFrame([time]).T, result], axis=1) 

#設定dataframe的column名稱
result.columns = ['time_index', 'signal_avg', 'signal_std', 'amplitude_avg', 'avg_peak']

#顯示最後結果
print('\n最後結果:\n' ,result)
#儲存成另一csv檔
result.to_csv("../OpenSignals_files/20231227/analysis/2023-12-27_20-55-13(eda_analysis).csv")
