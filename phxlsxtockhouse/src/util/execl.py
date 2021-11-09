# /usr/local/bin/python3
import re
import openpyxl
from math import floor


class Excel:

    def __init__(self, path, sheet_name, skip_first, skip_next, mapper, g_batch_size):
        self.wb = openpyxl.load_workbook(filename=path, read_only=True, keep_links=False, data_only=True)
        self.ws = self.wb[sheet_name]
        self.title_row = skip_first
        self.skip_next = skip_next
        self.mapper = mapper
        self.g_batch_size = g_batch_size
        self.dim = self.calCellsRange(self.ws.calculate_dimension())
        self.adapted_mapper = self.mapperAdapter(self.mapper, self.title_row, self.dim['left'], self.dim['right'])
        adapted_mapper = set(map(lambda item: item["des"], self.adapted_mapper))
        dim_mapper = set(map(lambda item: item["des"], self.mapper))
        # print("mapper \n")
        # print(mapper)
        # print("Alex")
        # print("DIM: =>")
        # print(self.dim)
        # print(dim_mapper)
        # print("ADA: =>")
        # print(self.adapted_mapper)
        # print(adapted_mapper)
        # 这里判断，判断输入的参数是不是在你的数据dim之内
        if len(dim_mapper - adapted_mapper) != 0:
            raise Exception("DIM Don't match")
        self.data_rows_count = self.calDataRowsCount(self.dim)
        self.step_indeies = self.buildBatchIndex()

    # 计算dimensions
    def calCellsRange(self, dim):
        [left_top, right_bottom] = dim.split(':')
        left = re.findall(r'[A-Z]+', left_top)[0]
        top = int(re.findall(r'\d+', left_top)[0])
        right = re.findall(r'[A-Z]+', right_bottom)[0]
        bottom = int(re.findall(r'\d+', right_bottom)[0])
        return {'left': left, 'top': top, 'right': right, 'bottom': bottom}

    # 总行数
    def calDataRowsCount(self, dim):
        return dim['bottom'] - (self.title_row + 1) + 1

    # header的索引，这里假设title只有一行
    def mapperAdapter(self, mapper, title_row, col_start, col_end):
        result = []
        header_cells = self.ws[self.dim['left'] + str(title_row) + ":" + self.dim['right'] + str(title_row)]

        print("alex read header")
        header = list(map(lambda item: {"value": item.value ,"column_letter": item.column_letter, "column": item.column - 1}, header_cells[0]))
        for index, item in enumerate(header):
            if item["value"] is None:
                item["value"] = "col_{0}".format(index)

        for iter_mapper in mapper:
            for iter_header in header:
                if iter_mapper['src'] == iter_header["value"]:
                    result.append(
                        {'des': iter_mapper['des'],
                         'letter': iter_header["column_letter"],
                         'column': iter_header["column"]})

        # for iter_mapper in mapper:
        #     for iter_header in header_cells[0]:
        #         print(iter_header.value)
        #         if iter_mapper['src'] == iter_header.value:
        #             result.append(
        #                 {'des': iter_mapper['des'],
        #                  'letter': iter_header.column_letter,
        #                  'column': iter_header.column - 1})

        return result

    # 分批的索引
    def buildBatchIndex(self):
        batch_count = floor(self.data_rows_count / self.g_batch_size) + 1
        step_indeies = []
        for index in range(0, batch_count):
            step_indeies.append(min(index * self.g_batch_size + self.g_batch_size + self.title_row + 1,
                                    self.data_rows_count + self.title_row + 1))
        return step_indeies

    def buildBatchCoordinate(self, dim, index_range):
        return dim['left'] + str(index_range.start) + ":" + dim['right'] + str(index_range.stop - 1)

    def batchReader(self, func):
        # rows = self.ws.iter_rows(self.title_row + self.skip_next + 1 + 1, max(self.step_indeies)) # 多加一个1，因为是1-base
        rows = self.ws.iter_rows(self.title_row + 1 + self.skip_next, max(self.step_indeies))
        batch_hit_time = 0
        # row_process_count = self.title_row + self.skip_next + 1 + 1
        row_process_count = self.title_row + self.skip_next
        values = []
        for row in rows:
            tmp = {}
            for col in self.adapted_mapper:
                value = row[col['column']].value
                tmp[col['des']] = "None" if value is None else value
            values.append(tmp)
            row_process_count += 1
            if row_process_count == self.step_indeies[batch_hit_time] - 1:
                func(values, self.adapted_mapper)
                values.clear()
                batch_hit_time = batch_hit_time + 1
                if batch_hit_time == len(self.step_indeies):
                    break

    @staticmethod
    def getSchema(path, sheet_name, skip_first):
        wb = openpyxl.load_workbook(filename=path, read_only=True, keep_links=False, data_only=True)
        ws = wb[sheet_name]
        rows = ws.iter_rows(min_row=skip_first, max_row=skip_first)
        cols = []
        for row in rows:
            for idx, cell in enumerate(row):
                if cell.value is None:
                    cell = "col_" + str(idx)
                    cols.append(cell)
                else:
                    cols.append(cell.value)
        return cols
