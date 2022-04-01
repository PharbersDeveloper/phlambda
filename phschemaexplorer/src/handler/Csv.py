from constants.Errors import Errors, FileNotFound, NotCsvFile
from handler.Strategy import Strategy
from openpyxl.utils.exceptions import InvalidFileException
import os
import csv
# import openpyxl
import constants.Common as Common
import logging


class Csv(Strategy):

    def __init__(self):
        pass

    def __get_data(self, temp_file, skip_next, out_number=0, **kwargs):
        skip_next = int(skip_next)
        out_number = int(out_number)
        out_num = out_number if out_number > 0 else 20
        data_list = []
        with open(temp_file, 'r') as f:
            reader = csv.reader(f)
            for i, rows in enumerate(reader):
                if i == 0:
                    schema = rows
                if i <= skip_next:
                    continue
                data_list.append(rows)
                if i >= out_num + skip_next:
                    break

        return {'readNumber': 1,
                'sheet': 'csv',
                'schema': schema,
                'data': data_list
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
