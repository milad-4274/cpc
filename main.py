import numpy as np
import pandas as pd

from io import BytesIO
from datetime import datetime, timedelta
from pathlib import Path
import seaborn as sn

from data import get_data, get_data_from_fxmarket
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

for cp in currancy_pairs:

    print(cp.code)

    time_period_in_days = cp.get_time_period()
    time_frame = cp.time_frame

    n_candles = int(time_period_in_days * 24 * 60 / time_frame)
    print("number of candles:", n_candles)


    data = get_data(file_path=cp.get_file_name() ,symbol=cp.code)
    df = pd.read_json(BytesIO(data))
    df.drop(["timeframe"],axis=1,inplace=True)

    df.drop_duplicates(["time"],inplace=True)
    df.sort_values(["time"],inplace=True)

    zero_diffs = df.diff()
    df["time"] = df["time"].apply( lambda x: datetime.fromtimestamp(x))

    end_time = df["time"].iloc[-1]
    start_time = end_time - timedelta(days=time_period_in_days)



    # df = df[df["time"] > start_time]
    print("before ", df.iloc[0])
    df = df.iloc[-n_candles:]
    print("after ", df.iloc[0])

    cp.set_dataframe(df)
    appended_data.update({cp.code: df.close.values})

    print(zero_diffs["time"].value_counts())
    print(df.shape)
    print("#"*30)

appended_data = pd.DataFrame(appended_data)

print(appended_data, appended_data.shape)

sn.heatmap(appended_data.corr(), cmap ="YlGnBu",annot=True)
plt.show()

# pairs = []

# for cp1 in currancy_pairs:
#     for cp2 in currancy_pairs:
#         if cp1 != cp2:
#             if (cp1,cp2) not in pairs and (cp2,cp1) not in pairs:
#                 pairs.append((cp1,cp2))

# print(pairs, len(pairs))

# for pair in pairs:
#     res = np.corrcoef(pair[0].get_dataframe()["close"], pair[1].get_dataframe()["close"])
#     print(f"correlation between {pair[0]} and {pair[1]} is {res} ")





# for cp in currancy_pairs[:1]:

#     print(cp.code)

#     time_period_in_days = cp.get_time_period()

#     now = datetime.now()
#     format = "%y-%m-%d"
    
#     end_time = now
#     while end_time.weekday() > 4:
#         print("going to yesterday")
#         end_time -= timedelta(days=1)
    
#     end_date = end_time.strftime(format)

#     start_date = (end_time - timedelta(days=time_period_in_days)).strftime(format)


#     # end_time = df["time"].iloc[-1]
#     # start_time = end_time - timedelta(days=time_period_in_days)

#     data = get_data_from_fxmarket(file_path=cp.get_file_name() ,symbol=cp.code,start_date=start_date,end_data=end_date,update=True)
#     df = pd.read_json(BytesIO(data))

#     # df.drop(["timeframe"],axis=1,inplace=True)

#     # df.drop_duplicates(["time"],inplace=True)
#     # df.sort_values(["time"],inplace=True)

#     # zero_diffs = df.diff()
#     # df["time"] = df["time"].apply( lambda x: datetime.fromtimestamp(x))




#     # df = df[df["time"] > start_time]

#     cp.set_dataframe(df)

#     # print(zero_diffs["time"].value_counts())
#     print(df.shape)
#     print("#"*30)



