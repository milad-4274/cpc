import io
from math import pi
import pandas as pd
from bokeh.plotting import figure, show, output_file
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path


def plot_candle(df, name="candlestick",result_folder="graphs"):


    inc = df.close > df.open
    dec = df.open > df.close
    w = 10000

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, min_width=1000, title
    = "Candlestick")
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3

    p.segment(df.time, df.high, df.time, df.low, color="black")
    p.vbar(df.time[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    # print(df["time"][inc])
    p.vbar(df.time[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    dir = Path(result_folder)
    if not dir.is_dir():
        Path.mkdir(dir)
    
    result_path = dir / Path(name+".html")

    output_file(result_path, title=name)
    show(p)

def plot_mean(df):
    plt.scatter(df["time"],df["low"]+df["high"]/2,s=1)
    plt.show()

def save_data(df,name="csv-data",suffix="csv"):
    df.to_csv(name+"."+suffix)

def price_corr(price_data):
    price_data = price_data.dropna()
    price_data.reset_index(drop=True)
    return price_data.corr()


def corr_in_time(currencies, number_of_data, column="Close"):
    if len(currencies) != 2:
        raise ValueError(f"correlation in time can be calculated only between two currencies, you entered {len(currencies)}")

    if column is None:
        return currencies[0].rolling(number_of_data).corr(currencies[1])
    else:
        return currencies[0][column].rolling(number_of_data).corr(currencies[1][column])