from pathlib import Path
import requests


def get_data(file_path="eur_usd.txt",url="http://195.248.242.134:8000/candlesticks/candle",sumbol="EURUSD"):
    update_data = False
    data_path = Path(file_path)
    if data_path.is_file() and not update_data:
        with open(data_path, "rb") as f:
            data = f.read()
    else:

        params = {
            "symbol":sumbol
        }
        request = requests.get(url,params=params, timeout=100)
        if request.status_code == 200:
            data = request.content
        else:
            raise RuntimeError("failed to get data")
        with open(data_path,"wb") as f:
            f.write(data)
    return data

