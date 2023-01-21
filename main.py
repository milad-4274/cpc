import numpy as np
import pandas as pd

from io import BytesIO
from datetime import datetime, timedelta
from pathlib import Path

from data import get_data
from utils import plot_mean, plot_candle, save_data
from model import CurrencyPair

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

time_period_in_days = 30

for cp in currancy_pairs:

    print(cp.code)

    time_period_in_days = cp.get_time_period()


    data = get_data(file_path=cp.get_file_name() ,sumbol=cp.code)
    df = pd.read_json(BytesIO(data))
    df.drop(["timeframe"],axis=1,inplace=True)

    df.drop_duplicates(["time"],inplace=True)
    df.sort_values(["time"],inplace=True)

    zero_diffs = df.diff()
    df["time"] = df["time"].apply( lambda x: datetime.fromtimestamp(x))

    end_time = df["time"].iloc[-1]
    start_time = end_time - timedelta(days=time_period_in_days)

    # print(df["time"].tail())
    # print(df["time"].iloc[0])
    # print(df["time"].iloc[-1])

    df = df[df["time"] > start_time]

    cp.set_dataframe(df)

    print(zero_diffs["time"].value_counts())
    print("#"*30)

print("im here")
print(currancy_pairs[0].get_dataframe().head())



