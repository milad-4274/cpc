

from pathlib import Path
from io import BytesIO


class CurrencyPair():
    def __init__(self,code, time_frame=2 ) -> None:
        self.code = code
        self.file_name = self.code.lower()[:3] + "_" + self.code.lower()[3:] 
        self.time_frame = time_frame
        self.is_dataframe_setted = False
    
    def set_dataframe(self, df):
        self.dataframe = df
        self.is_dataframe_setted = True
    
    def get_dataframe(self):
        if not self.is_dataframe_setted:
            raise RuntimeError("dataframe not setted yet")
        else:
            return self.dataframe

    def update_timeframe(self, df, time_frame):
        self.set_dataframe(df)
        self.time_frame = time_frame

    
    def get_time_period(self):
        time_table = {
            2 : 30,
            5 : 30,
            10 : 60,
            15 : 60,
            30 : 60,
            60 : 90,
            240 : 180,
            1440 : 365
        }
        return time_table[self.time_frame]

    def get_file_name(self, suffix="txt"):
        return f"{self.file_name}_{self.time_frame}.{suffix}"

    def save_data(self, data_dir):
        data_dir = Path(data_dir)
        if not data_dir.is_dir():
            Path.mkdir(data_dir)
        
        data_path = data_dir / Path(self.get_file_name())
        data = self.get_dataframe()
        with open(data_path,"w") as f:
            # f.write(data)
            # f.write(data.to_json())
            data.apply(lambda x: f.write(x.to_json()), axis=1)
        

    def __str__(self):
        return self.code

