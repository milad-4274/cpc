import numpy as np
import pandas as pd

import yfinance as yf
import plotly.graph_objs as go
import yaml
from collections import defaultdict
import seaborn as sn
import matplotlib.pyplot as plt
from pathlib import Path

from model import CurrencyPair
from utils import price_corr


plt.rcParams['figure.figsize'] = [8.0, 8.0]

with open("config.yaml", "r") as yaml_file:
    cfg = yaml.load(yaml_file, Loader=yaml.FullLoader)

update_data = cfg["user_input"]["update_data"]
currency_pairs_input = cfg["user_input"]["currency_pairs"]
time_frames = cfg["user_input"]["time_frames"] 
# print(time_frames,type(time_frames))
# periods = cfg["user_input"]["periods"]
data_dir = cfg["pathes"]["data_path"]
graph_dir = cfg["pathes"]["graph_path"]


currency_pairs = []

for cp in currency_pairs_input:
    for tf in time_frames:
        cp_object = CurrencyPair(cp,tf)
        cp_object.period = time_frames[tf]
        currency_pairs.append(cp_object)



price_data = defaultdict(dict)
smallest_data = np.inf

valid_intervals = ["1m","2m","5m","15m","30m","60m","90m","1h","1d","5d","1wk","1mo","3mo"]

for cp in currency_pairs:

    #Download JPYAUD data
    print(cp.code, "___", cp.time_frame)
    # print(type(cp.time_frame))
    if cp.time_frame in valid_intervals:
        print(cp.time_frame, cp.period)
        data = yf.download(tickers = cp.code + "=X" ,period =cp.period, interval = cp.time_frame)
        
    else:
        print(cp.time_frame + " is not valid for yahoo finance, creating it")
        continue
    if data.empty:
        raise ValueError("data is empty")

    print(data.head())
    print(data.tail())
    print(data.shape)

    smallest_data = data.shape[0] if data.shape[0] < smallest_data else smallest_data
    price_data[cp.time_frame][cp.code] = data["Close"]

    cp.set_dataframe(pd.DataFrame(price_data))

    #declare figure
    # fig = go.Figure()

    # #Candlestick
    # fig.add_trace(go.Candlestick(x=data.index,
    #                 open=data['Open'],
    #                 high=data['High'],
    #                 low=data['Low'],
    #                 close=data['Close'], name = 'market data'))

    # # Add titles
    # fig.update_layout(
    #     title=cp.code)

    #Show
    # fig.show()

print("len ", smallest_data)

# for key, values in price_data.items():
#     price_data[key] = values[-smallest_data:]

# price_data = pd.DataFrame(price_data)
# price_data = price_data.dropna()
# price_data.reset_index(drop=True)


for tf in price_data:
    corr = price_corr(pd.DataFrame(price_data[tf]))
    sn.heatmap(corr, cmap ="YlGnBu",annot=True)
    cp_info = f"time_frame: {tf}, period: {time_frames[tf]}"
    time_info = f"start_time: {price_data[tf][list(price_data[tf].keys())[0]].index[0]}\n end_time:{price_data[tf][list(price_data[tf].keys())[0]].index[-1]}"
    plt.title(cp_info + time_info)
    plt.savefig(Path(graph_dir) / (cp_info + ".png"))
    plt.show()


# print(price_data.shape)
# print(price_data.head)
# print(price_data.corr())

#TODO handle connection error for one of the cp objs
#TODO resampling to create missed timeframes