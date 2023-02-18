import pandas as pd
import matplotlib.pyplot as plt

from utils import price_corr, corr_in_time

data1 = pd.read_json("data\EURUSD_H1.json")
data2 = pd.read_json("data\GBPUSD_H1.json")


number_of_days = 30
data_per_day = 30 * 24
cor_time = corr_in_time([data1, data2], data_per_day * number_of_days, "close")
cor_time.dropna(inplace=True)
print(cor_time.iloc[0])
print(len(cor_time))
cor_time.plot()
plt.show()

