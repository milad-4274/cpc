import numpy as np
import pandas as pd
import yaml

from io import BytesIO
from datetime import datetime, timedelta
from pathlib import Path
import seaborn as sn

import sys

from data import get_data, get_data_from_fxmarket, resample_timeframe, pearson_corr, crosscorr_between_two_data, windowed_time_lagged_cc, dtw_corr
from utils import plot_mean, plot_candle, save_data
from model import CurrencyPair
import matplotlib.pyplot as plt

with open("config.yaml", "r") as yaml_file:
    cfg = yaml.load(yaml_file, Loader=yaml.FullLoader)

update_data = cfg["user_input"]["update_data"]
currency_pairs_input = cfg["user_input"]["currency_pairs"]
time_frames = cfg["user_input"]["time_frames"] 
data_dir = cfg["pathes"]["data_path"]
graph_dir = cfg["pathes"]["graph_path"]

print(time_frames)
currency_pairs = []

for cp in currency_pairs_input:
    cp_object = CurrencyPair(cp)
    currency_pairs.append(cp_object)


price_values = {}

for cp in currency_pairs:


    time_period_in_days = cp.get_time_period()
    time_frame = cp.time_frame

    n_candles = int(time_period_in_days * 24 * 60 / time_frame)
    print("number of candles:", n_candles)

    # get data locally if update_data id False else get newer data from api
    data = get_data(data_dir, file_path=cp.get_file_name() ,symbol=cp.code, update= update_data)

    # creating dataframe
    df = pd.read_json(BytesIO(data))

    # cleaning data
    df.drop(["timeframe"],axis=1,inplace=True)
    df.drop_duplicates(["time"],inplace=True)
    df.sort_values(["time"],inplace=True)
    df["time"] = df["time"].apply( lambda x: datetime.fromtimestamp(x))


    zero_diffs = df.diff()
    
    # extracting candles we need to check
    df = df.iloc[-n_candles:]

    # add dataframe to currencyPair object
    cp.set_dataframe(df)
    price_values.update({cp.code: df.close.values})



    # new = resample_timeframe(df,"2min","1D")
    # cp.update_timeframe(new,1440)
    # cp.save_data(data_dir)
    # print("shapeee", df.shape, new.shape)

    # print(zero_diffs["time"].value_counts())
    # print(df.shape)
    # print(new.head())
    # print(new.columns)
    # plot_candle(df,f"{cp.code}_M2")
    # plot_candle(new,f"{cp.code}_M10")
    # print("#"*30)

price_values = pd.DataFrame(price_values)

print(price_values, price_values.shape)

sn.heatmap(pearson_corr(price_values), cmap ="YlGnBu",annot=True)
# sn.heatmap(pearson_corr(price_values.diff()), cmap ="YlGnBu",annot=True)
# crosscorr_between_two_data(price_values["EURUSD"],price_values["GBPUSD"],100)
# windowed_time_lagged_cc(price_values)
# dtw_corr(price_values)
# TODO sn.heatmap(person_corr_stationary(price_values), cmap= "YlGnBu", annot=True)
# TODO handle resampling data scenario, maybe every time you're updating data it should happen



plt.show()

sn.heatmap(pearson_corr(price_values.diff().dropna()), cmap ="YlGnBu",annot=True)

plt.show()