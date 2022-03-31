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

    def __get_data(self, temp_file, skip_next, out_number=0, **kwargs):
        skip_next = int(skip_next)
        out_number = int(out_number)
        out_num = out_number if out_number > 0 else 20
        print(os.popen('ls').read())
        print(os.popen('pwd').read())
        data = pd.read_csv(temp_file, encoding="utf-8")
        body = data.values.tolist()
        body = body[skip_next:]
        body = body[:out_num]
        return {'readNumber': 1,
                'sheet': 'csv',
                'schema': data.columns.values.tolist(),
                'data': body
                }

    def do_exec(self, data):
        logging.debug("Excel Xlsx === \n")
        logging.debug(data)

        try:
            project = data["project"]
            temp_file = data["tempfile"]
            path = f"{os.environ.get(Common.PATH_PREFIX).format(project)}{temp_file}"
            csv_data = self.__get_data(temp_file=path, **data)

        except FileNotFoundError as e:
            raise FileNotFound(e)
        except InvalidFileException as e:
            raise NotCsvFile(e)
        except Exception as e:
            raise Errors(e)

        return {
            'sheets': ["csv"],
            'body': [csv_data]
            }
