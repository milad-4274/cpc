

class CurrencyPair():
    def __init__(self,file_name, code, time_frame=2 ) -> None:
        self.file_name = file_name
        self.code = code
        self.time_frame = time_frame
        self.is_dataframe_setted = False
    
    def set_dataframe(self, df):
        self.dataframe = df
        self.is_dataframe_setted = True
    
    def get_dataframe(self):
        if self.is_dataframe_setted:
            raise RuntimeError("dataframe not setted yet")
        else:
            return self.dataframe
    
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
        return self.file_name + "." + suffix