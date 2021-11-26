import pandas as pd
from Strategy import Strategy


class CsvStrategy(Strategy):

    def do_exec(self, data):

        print("Csv")
