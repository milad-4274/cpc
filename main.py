import numpy as np
import pandas as pd

from io import BytesIO
from datetime import datetime, timedelta
from pathlib import Path
import seaborn as sn

from data import get_data, get_data_from_fxmarket, resample_timeframe
from utils import plot_mean, plot_candle, save_data
from model import CurrencyPair
import matplotlib.pyplot as plt

currancy_pairs = {
    "eur_usd": "EURUSD",
    "gbp_usd": "GBPUSD",
    "usd_chf": "USDCHF",
    "aud_usd": "AUDUSD",
    "usd_cad": "USDCAD",
    "usd_jpy": "USDJPY"
}
print("processing ...")
print("#"*30)

euro_usd = CurrencyPair("eur_usd","EURUSD")
gbp_usd = CurrencyPair("gbp_usd","GBPUSD")
usd_chf = CurrencyPair("usd_chf","USDCHF")
aud_usd = CurrencyPair("aud_usd","AUDUSD")
usd_cad = CurrencyPair("usd_cad","USDCAD")
usd_jpy = CurrencyPair("usd_jpy","USDJPY")

currancy_pairs = [euro_usd, gbp_usd, usd_chf, aud_usd, usd_cad, usd_jpy]

appended_data = {}

data_dir = "data"

for cp in currancy_pairs:

    print(cp.code)

    time_period_in_days = cp.get_time_period()
    time_frame = cp.time_frame

    n_candles = int(time_period_in_days * 24 * 60 / time_frame)
    print("number of candles:", n_candles)


    data = get_data(data_dir, file_path=cp.get_file_name() ,symbol=cp.code)
    df = pd.read_json(BytesIO(data))
    df.drop(["timeframe"],axis=1,inplace=True)

    df.drop_duplicates(["time"],inplace=True)
    df.sort_values(["time"],inplace=True)

    zero_diffs = df.diff()
    df["time"] = df["time"].apply( lambda x: datetime.fromtimestamp(x))


    print("before ", df.iloc[0])
    df = df.iloc[-n_candles:]
    print("after ", df.iloc[0])

    cp.set_dataframe(df)
    appended_data.update({cp.code: df.close.values})

    new = resample_timeframe(df,"2min","1D")
    cp.update_timeframe(new,1440)
    cp.save_data(data_dir)
    print("shapeee", df.shape, new.shape)

    # print(zero_diffs["time"].value_counts())
    # print(df.shape)
    print(new.head())
    print(new.columns)
    plot_candle(df,f"{cp.code}_M2")
    plot_candle(new,f"{cp.code}_M10")
    print("#"*30)

appended_data = pd.DataFrame(appended_data)

print(appended_data, appended_data.shape)

sn.heatmap(appended_data.corr(), cmap ="YlGnBu",annot=True)
plt.show()
