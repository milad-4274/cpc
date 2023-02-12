import plotly.graph_objs as go
from pathlib import Path

def plot_candles(dataframe, currency_pair, show=False, write=True, path=None):
    fig = go.Figure()

    #Candlestick
    fig.add_trace(go.Candlestick(x=dataframe.index,
                    open=dataframe['Open'],
                    high=dataframe['High'],
                    low=dataframe['Low'],
                    close=dataframe['Close'], name = 'market data'))

    # Add titles
    fig.update_layout(
        title=currency_pair.code)

    # fig.write_image(Path(path) / (currency_pair.code + currency_pair.time_frame + period + ".png"))
    if write:
        fig.write_image(Path(path))

    if show:
        fig.show()
