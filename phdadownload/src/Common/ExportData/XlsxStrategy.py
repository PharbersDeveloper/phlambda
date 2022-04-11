
import pandas as pd
from Common.ExportData.__init__ import Strategy


class XlsxStrategy(Strategy):

    def __init__(self):
        pass

    def do_exec(self, fin_list, file_name, schema):
        print("do_exec-----------------4------------"*5)
        dataf = pd.DataFrame(fin_list)
        dataf.columns = schema
        print("do_exec-----------------before_save------------"*5)
        dataf.to_excel(file_name, index=False)
        print("do_exec-----------------5------------"*5)
