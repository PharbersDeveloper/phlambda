
import pandas as pd
from __init__ import Strategy


class XlsxStrategy(Strategy):

    def __init__(self):
        pass

    def do_exec(self, fin_list, file_name, schema):
        dataf = pd.DataFrame(fin_list)
        dataf.columns = schema
        writer = pd.ExcelWriter(file_name)
        dataf.to_excel(writer, sheet_name='Data1', index=False)
        writer.save()
