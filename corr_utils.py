import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def compute_correlation(
        df1: pd.DataFrame,
        df2: pd.DataFrame, 
        period: int, 
        column: str = "close") -> float:
    """
    calculating correlation between two dataframe columns, assuming dataframes have OHLC data \n
    inputs:
        - df1: first dataframe
        - df2: second dataframe
        - period: the number of data(candles) you want to use for computing correlation
        - column: which of column is choosed for calculating correlation. default close 
    \n
    output:
        - correlation of two dataframes column in the period
    """
    first_df, second_df = df1.copy(), df2.copy()
    first_df.columns = first_df.columns.str.lower()
    second_df.columns = second_df.columns.str.lower()
    corr = df1["close"].iloc[-period:].corr(df2["close"].iloc[-period:])

    return corr

def rolling_correlation(
        df1: pd.DataFrame, 
        df2: pd.DataFrame, 
        period: int, 
        column: str = "close") -> pd.DataFrame:
    """
    calculating rolling correlation between two dataframe columns, assuming dataframes have OHLC data \n
    inputs:
        - df1: first dataframe
        - df2: second dataframe
        - period: the number of data(candles) you want to use as rolling variable 
        - column: which of column is choosed for calculating correlation. default close 
    \n
    output:
        - pandas dataframe of rolling correlation 
    """
    first_df, second_df = df1.copy(), df2.copy()
    first_df.columns = first_df.columns.str.lower()
    second_df.columns = second_df.columns.str.lower()
    column = column.lower()

    corr_roll = first_df[column].rolling(period, min_periods=int(period*0.5)).corr(second_df[column])

    if corr_roll.isnull().all():
        raise ValueError("It seems there is problem in input data, more than 50 percent of data index are mismatch")
    

    return corr_roll




if __name__ == "__main__":

    # testing function performances in this file (not executing if you import this file)

    #reading data
    from pathlib import Path
    import numpy as np
    data_path = Path("data")
    data1_name = "AUDUSD_M2.json"
    data2_name = "EURUSD_M2.json"

    df1 = pd.read_json(data_path / data1_name)
    df2 = pd.read_json(data_path / data2_name)

    # converting datetime to timestamp (s)
    df1["datetime"] = df1["datetime"].values.astype(np.int64) / 10**9
    df2["datetime"] = df2["datetime"].values.astype(np.int64) / 10**9

    # number of expected candles in day for timeframe 2M
    data_per_day = 30 * 24
    
    corr = compute_correlation(df1, df2, period= 2* data_per_day, column="close")

    df1.set_index("datetime", inplace=True)
    df2.set_index("datetime", inplace=True)

    roll_corr = rolling_correlation(df1, df2, data_per_day * 60, column="close")

    roll_corr.plot()
    plt.show()