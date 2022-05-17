
from Common.ExportData.__init__ import Strategy
import pandas as pd


class CsvStrategy(Strategy):

    def __init__(self):
        pass

    def do_exec(self, fin_list, file_name, schema):
        dataf = pd.DataFrame(fin_list)
        dataf.columns = schema
        dataf.to_csv(file_name, index=False)
