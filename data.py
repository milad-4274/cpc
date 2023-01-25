from pathlib import Path
import requests


def get_data(data_dir= "data", file_path="eur_usd.txt",url="http://195.248.242.134:8000/candlesticks/candle",symbol="EURUSD",update=False):
    data_dir = Path(data_dir)
    if not data_dir.is_dir():
        Path.mkdir(data_dir)
    data_path = data_dir / Path(file_path)
    if data_path.is_file() and not update:
        with open(data_path, "rb") as f:
            data = f.read()
    else:

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