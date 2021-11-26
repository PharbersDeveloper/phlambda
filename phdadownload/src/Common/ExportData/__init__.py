import boto3
from abc import ABC, abstractmethod
from clickhouse_driver import Client


class Strategy(ABC):
    client = Client(host='127.0.0.1', port='9000')

    @abstractmethod
    def do_exec(self, data):
        pass

    def read_sql(self, sql):
        data = self.client.execute(sql, columnar=True)
        return data

    def parse_data(self, schema, down_data):
        final_list = [schema]
        for i in range(len(down_data[0])):
            first_list = []
            for j in down_data:
                first_list.append(str(j[i]))
            final_list.append(first_list)
        print(final_list)
        return final_list

    def run(self, sql, schema, file_name, **kwargs):
        path_file_name = f'/tmp/{file_name}'

        down_data = self.read_sql(sql)
        fin_list = self.parse_data(schema, down_data)
        self.do_exec(fin_list, path_file_name, schema)
        return self.to_s3(path_file_name, file_name)

    def to_s3(self, path_file_name, file_name):
        s3 = boto3.client('s3')
        s3.upload_file(path_file_name, 'ph-platform', f'2020-11-11/template/download_test/{file_name}')
        return s3.generate_presigned_url('get_object', Params={'Bucket': 'ph-platform',
                                        'Key': f"2020-11-11/template/download_test/{file_name}"},
                                         ExpiresIn=3600, HttpMethod="get")
