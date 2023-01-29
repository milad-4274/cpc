from pathlib import Path
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def get_data(data_dir= "data", file_path="eur_usd.txt",url="http://195.248.242.134:8000/candlesticks/candle",symbol="EURUSD",update=False):
    data_dir = Path(data_dir)
    if not data_dir.is_dir():
        Path.mkdir(data_dir)
    data_path = data_dir / Path(file_path)
    if data_path.is_file() and not update:
        print("reading data locally")
        with open(data_path, "rb") as f:
            data = f.read()
    else:
        print("sending request to getting data")
        params = {
            "symbol":symbol
        }
        request = requests.get(url,params=params, timeout=100)
        if request.status_code == 200:
            data = request.content
        else:
            raise RuntimeError("failed to get data")
        with open(data_path,"wb") as f:
            f.write(data)
    return data


def get_data_from_fxmarket(file_path, symbol, start_date, end_data, update=False ):
    api_key = "cQPEWXgsqZFNi0P0Dffo"
    url = "https://fxmarketapi.com/apipandas"
    data_path = Path(file_path)

    if data_path.is_file() and not update:
        with open(data_path, "rb") as f:
            data = f.read()
    else:
        params = {'currency' : symbol,
                'start_date' : start_date,
                'end_date': end_data,
                'api_key':api_key,
                # 'interval' : 'daily'
                }
        request = requests.get(url, params=params)
        if request.status_code == 200:
            data = request.content
        else:
            print(request.content)
            raise RuntimeError("failed to get data")
        with open(data_path,"wb") as f:
            f.write(data)
    return data


def resample_timeframe(df, curr_timeframe, new_timeframe):
    ohlc_dict = {                                                                                                             
        'open': 'first',                                                                                                    
        'high': 'max',                                                                                                       
        'low': 'min',                                                                                                        
        'close': 'last',
    }

    new = df.set_index("time").resample(new_timeframe, closed='left', label='left').apply(ohlc_dict)
    new.insert(0, 'time', new.index)
    new.reset_index(drop=True)
    return new

def pearson_corr(df):
    return df.corr()

def crosscorr(datax, datay, lag=0, wrap=False):
    """ Lag-N cross correlation. 
    Shifted data filled with NaNs 
    
    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length
    Returns
    ----------
    crosscorr : float
    """
    if wrap:
        shiftedy = datay.shift(lag)
        shiftedy.iloc[:lag] = datay.iloc[-lag:].values
        return datax.corr(shiftedy)
    else: 
        return datax.corr(datay.shift(lag))

def crosscorr_between_two_data(datax, datay,maxlags):

    rs = [crosscorr(datax,datay, lag) for lag in range(-int(maxlags),int(maxlags))]
    offset = np.floor(len(rs)/2)-np.argmax(rs)
    f,ax=plt.subplots(figsize=(14,3))
    ax.plot(rs)
    ax.axvline(np.ceil(len(rs)/2),color='k',linestyle='--',label='Center')
    ax.axvline(np.argmax(rs),color='r',linestyle='--',label='Peak synchrony')
    # ax.set(title=f'Offset = {offset} frames\nS1 leads <> S2 leads', xlabel='Offset',ylabel='Pearson r')
    # ax.set_xticks([0, 50, 100, 151, 201, 251, 301])
    # ax.set_xticklabels([-150, -100, -50, 0, 50, 100, 150]);
    plt.legend()

def windowed_time_lagged_cc(df):
    # Windowed time lagged cross correlation
    seconds = 5
    fps = 30
    no_splits = 20
    samples_per_split = df.shape[0]/no_splits
    rss=[]
    for t in range(0, no_splits):
        d1 = df['EURUSD'].loc[(t)*samples_per_split:(t+1)*samples_per_split]
        d2 = df['GBPUSD'].loc[(t)*samples_per_split:(t+1)*samples_per_split]
        rs = [crosscorr(d1,d2, lag) for lag in range(-int(seconds*fps),int(seconds*fps+1))]
        rss.append(rs)
    rss = pd.DataFrame(rss)
    f,ax = plt.subplots(figsize=(10,5))
    sns.heatmap(rss,cmap='RdBu_r',ax=ax)
    ax.set(title=f'Windowed Time Lagged Cross Correlation',xlim=[0,301], xlabel='Offset',ylabel='Window epochs')
    ax.set_xticks([0, 50, 100, 151, 201, 251, 301])
    ax.set_xticklabels([-150, -100, -50, 0, 50, 100, 150]);

    # Rolling window time lagged cross correlation
    seconds = 5
    fps = 30
    window_size = 300 #samples
    t_start = 0
    t_end = t_start + window_size
    step_size = 30
    rss=[]
    while t_end < 5400:
        d1 = df['EURUSD'].iloc[t_start:t_end]
        d2 = df['GBPUSD'].iloc[t_start:t_end]
        rs = [crosscorr(d1,d2, lag, wrap=False) for lag in range(-int(seconds*fps),int(seconds*fps+1))]
        rss.append(rs)
        t_start = t_start + step_size
        t_end = t_end + step_size
    rss = pd.DataFrame(rss)

    f,ax = plt.subplots(figsize=(10,10))
    sns.heatmap(rss,cmap='RdBu_r',ax=ax)
    ax.set(title=f'Rolling Windowed Time Lagged Cross Correlation',xlim=[0,301], xlabel='Offset',ylabel='Epochs')
    ax.set_xticks([0, 50, 100, 151, 201, 251, 301])
    ax.set_xticklabels([-150, -100, -50, 0, 50, 100, 150]);

from dtw import dtw,accelerated_dtw

def dtw_corr(df):
    d1 = df['EURUSD'].interpolate().values
    d2 = df['GBPUSD'].interpolate().values
    print("we have d1 and d2")
    d, cost_matrix, acc_cost_matrix, path = accelerated_dtw(d1,d2, dist='euclidean')
    print("acc cost and path calculated")

    plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
    plt.plot(path[0], path[1], 'w')
    plt.xlabel('Subject1')
    plt.ylabel('Subject2')
    plt.title(f'DTW Minimum Path with minimum distance: {np.round(d,2)}')
    # plt.show()