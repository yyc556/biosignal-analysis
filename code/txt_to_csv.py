import pandas as pd


#從txt中取出資料
def get_txt_data(path):
    time = []
    ecg = []
    eda = []
    with open(path, 'r') as f:
        for line in f.readlines():
            #print(line)
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
    data = pd.DataFrame({'time':time, 'eda':eda, 'ecg':ecg})
    print(data)
    return data
    
    
p = '../biomarkers/formal data/0522 P15/opensignals_0007804B2C0E_'

file_list = ['13-28-03', '13-54-08', '14-04-47', '14-26-41', '14-52-26', '14-58-02']   # 與合併的資料檔名(日期時間)


time = []

'''
#各段訊號各別轉成csv
i = 0
for name in file_list:
    i += 1
    df = pd.DataFrame()
    df = get_txt_data(p + name + '_converted.txt')
    df.to_csv('../biomarkers/formal data/csv data/P17_s' + str(i) + '.csv')
    time.append(len(df)-1)
    
print(time)
'''

#合併整段並輸出csv
final = pd.DataFrame()
for i in range(6):
    print(file_list[i])
    df = pd.DataFrame()
    df = get_txt_data(p + file_list[i] + '_converted.txt')
    df['session'] = i+1
    final = pd.concat([final, df])

final = final.reset_index(drop=True)
#輸出成一個合併過後的csv檔
print(final)
final.to_csv('../結案報告/0716/P15 data/P15_WithoutTest.csv')


