from Strategy import Strategy
import pandas as pd


class XlsxStrategy(Strategy):

    def __init__(self):
        pass

    def do_exec(self, data):
        sql = data["sql"]
        schema = data["schema"]
        print("Excel")
