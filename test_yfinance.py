# Raw Package
import numpy as np
import pandas as pd
#Data Source
import yfinance as yf
#Data viz library
import plotly.graph_objs as go
import yaml
from model import CurrencyPair
from collections import defaultdict


with open("config.yaml", "r") as yaml_file:
    cfg = yaml.load(yaml_file, Loader=yaml.FullLoader)

update_data = cfg["user_input"]["update_data"]
currency_pairs_input = cfg["user_input"]["currency_pairs"]
time_frames = cfg["user_input"]["time_frames"] 
data_dir = cfg["pathes"]["data_path"]
graph_dir = cfg["pathes"]["graph_path"]


currency_pairs = []

for cp in currency_pairs_input:
    for tf in time_frames:
        cp_object = CurrencyPair(cp,tf)
        currency_pairs.append(cp_object)


price_data = defaultdict(dict)
smallest_data = np.inf

for cp in currency_pairs:

    #Download JPYAUD data
    print(cp.code, "___", cp.time_frame)
    print(type(cp.time_frame))
    data = yf.download(tickers = cp.code + "=X" ,period ='max', interval = cp.time_frame)
    if data.empty:
        raise ValueError("could not to download data")

    print(data.head())
    print(data.tail())
    print(data.shape)

    smallest_data = data.shape[0] if data.shape[0] < smallest_data else smallest_data
    price_data[cp.time_frame][cp.code] = data["Close"]

    #declare figure
    fig = go.Figure()

    #Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'], name = 'market data'))

    # Add titles
    fig.update_layout(
        title=cp.code)

    #Show
    # fig.show()

print("len ", smallest_data)

# for key, values in price_data.items():
#     price_data[key] = values[-smallest_data:]

price_data = pd.DataFrame(price_data)
price_data = price_data.dropna()
price_data.reset_index(drop=True)

print(price_data.shape)
print(price_data.head)
print(price_data.corr())