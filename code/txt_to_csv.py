time = []
ecg = []
eda = []

#從txt中取出資料
with open('../OpenSignals_files/20231219/raw data/opensignals_0007804b2c0e_2023-12-19_14-14-45_converted.txt', 'r') as f:
    for line in f.readlines():
        print(line)
        if line[0]!="#":   #只讀取數據的部分
            line = line.strip('\n')  #去掉列表中每一個元素的换行符
            line = line.strip('\t')  #去掉列表中每一個元素的tab符
            
            space1 = line.find('	')
            time.append(float(line[:space1]))   #取出"時間"資料(將資料從string轉成float)
            temp = line[space1+1:]   #紀錄剩下未讀取的資料
            temp = temp[3+1:]   #先去除"0.0“部分
            space2 = temp.find('	') 
            eda.append(float(temp[:space2]))   #取出"EDA"資料(將資料從string轉成float)
            ecg.append(float(temp[space2+1:]))   #取出"ECG"資料(將資料從string轉成float)

#建立dataframe
import pandas as pd
data = pd.DataFrame({'time':time, 'ecg':ecg, 'eda':eda})
#輸出成一個csv檔
data.to_csv("../OpenSignals_files/20231219/2023-12-19_14-14-45(converted).csv")
print(data)
