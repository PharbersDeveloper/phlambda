from Strategy import Strategy

from constants.Errors import Errors, FileNotFound, NotCsvFile
from handler.Strategy import Strategy
from openpyxl.utils.exceptions import InvalidFileException
import os
# import openpyxl
import constants.Common as Common
import logging
import pandas as pd


class Csv(Strategy):

    def __init__(self):
        pass

    def do_exec(self, data):
        logging.debug("Excel Xlsx === \n")
        logging.debug(data)


        result = {}
        try:
            skip_first = data["skip_first"]
            skip_next = data["skip_next"]
            project = data["project"]
            temp_file = data["tempfile"]

            // csv

            result["sheets"] = ["csv"]
            result["body"] = # TODO: ...
        except FileNotFoundError as e:
            raise FileNotFound(e)
        except InvalidFileException as e:
            raise NotCsvFile(e)
        except Exception as e:
            raise Errors(e)

        return result
