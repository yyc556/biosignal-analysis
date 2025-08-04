import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler



data = pd.read_csv("../結案報告/0716/P12 data/P12_WithoutTest.csv")

signal = data['eda']

#減掉baseline
baseline = np.mean(signal[:252150])
signal = signal - baseline

#standardization
data_array = np.array(signal).reshape(-1, 1)
scaler = StandardScaler()
signal = scaler.fit_transform(data_array)

time = data.index.values


fig = plt.figure(figsize=(21,5))
plt.plot(time, signal, color='#0C81BE')
plt.axvline(252150, color='gray')  #part1
plt.axvline(904500, color='gray')  #par2
plt.axvline(1854600, color='gray') #part2-mission
plt.axvline(3510450, color='gray') #part3
plt.axvline(3829400, color='gray') #part3-mission
plt.xlabel('time index')
plt.ylabel('signal')
plt.title("EDA signal", loc='left', fontsize = 15, weight='bold')
plt.savefig('../結案報告/0716/P12 data/P12 EDA signal(-base,std).png', dpi=600)