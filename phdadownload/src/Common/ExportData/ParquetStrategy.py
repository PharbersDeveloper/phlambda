
from __init__ import Strategy
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

class ParquetStrategy(Strategy):

    def __init__(self):
        pass

    def do_exec(self, fin_list, file_name, schema):
        dataf = pd.DataFrame(fin_list)
        dataf.columns = schema
        dataf.to_parquet(file_name, index=False)

        # t_file = 'test.parquet'
        # array = [1, 2, 3, 4]
        #
        # df = pd.DataFrame(array)
        # # Create a parquet table from your dataframe
        # table = pa.Table.from_pandas(df)
        # # Write direct to your parquet file
        # pq.write_table(table, t_file)
        #
        # # write to this dir and auto name the parquet file
        # out_path = '.'
        # pq.write_to_dataset(table, root_path=out_path)


    # def do_exec(self, data):
        # sql = data["sql"]
        # schema = data["schema"]
        # print(self.read_sql(sql))
        # down_data = self.read_sql(sql)
        # print("Parquet")
        # last_list = []
        # for i in range(6):
        #     first_list = []
        #     for j in down_data:
        #         first_list.append(j[i])
        #     last_list.append(first_list)
        # print(last_list)
        #
        #
        #
        #
        # dataf = pd.DataFrame(last_list)
        # print(dataf)
        # # 创建excel
        # writer = pd.ExcelWriter("test11.xlsx")
        # dataf.to_excel(writer, sheet_name='Data1', index=False)
        # writer.save()
        #
        # t_file = 'test.parquet'
        # array = [1, 2, 3, 4]
        #
        # df = pd.DataFrame(array)
        # # Create a parquet table from your dataframe
        # table = pa.Table.from_pandas('DataFrame', dataf)
        # # Write direct to your parquet file
        # pq.write_table(table, out_file)
        #
        # # write to this dir and auto name the parquet file
        # out_path = './database/'
        # pq.write_to_dataset(table, root_path=out_path)

        # s3 = boto3.client('s3')
        #
        # s3.upload_file('test11.xlsx', 'ph-platform', '2020-11-11/template/download_test/test1.xlsx')
        #
        # s3.generate_presigned_url('get_object', Params={'Bucket': 'ph-platform', 'Key': "2020-11-11/template/download_test/test.xlsx"}, ExpiresIn=3600, HttpMethod="get")
# print(s3.upload_file('test11.xlsx', 'ph-platform', '2020-11-11/template/download_test/test2.xlsx'))


