import boto3
import json
from abc import ABC, abstractmethod
from clickhouse_driver import Client


class Strategy(ABC):

    @abstractmethod
    def do_exec(self, data):
        pass

    def read_sql(self, sql, project):
        # ssm get url
        ssm_client = boto3.client('ssm')
        response = ssm_client.get_parameter(
            Name='project_dirver_args',
            WithDecryption=True|False
        )
        ssm_dict = json.loads(response.get('Parameter').get('Value'))
        url = ssm_dict.get(project)
        client = Client(host=url[7:-5], port=url[-4:])
        data = client.execute(sql, columnar=True)
        return data

    def parse_data(self, schema, down_data):
        final_list = []
        for i in range(len(down_data[0])):
            first_list = []
            for j in down_data:
                first_list.append(str(j[i]))
            final_list.append(first_list)
        return final_list

    def run(self, schema, file_name, category, **kwargs):
        file_name = file_name + '.' + category
        path_file_name = f'/tmp/{file_name}'

        down_data = self.read_sql(**kwargs)
        fin_list = self.parse_data(schema, down_data)
        self.do_exec(fin_list, path_file_name, schema)
        return self.to_s3(path_file_name, file_name)

    def to_s3(self, path_file_name, file_name):
        s3 = boto3.client('s3')
        s3.upload_file(path_file_name, 'ph-platform', f'2020-11-11/download/{file_name}')
        return s3.generate_presigned_url('get_object', Params={'Bucket': 'ph-platform',
                                        'Key': f"2020-11-11/download/{file_name}"},
                                         ExpiresIn=3600, HttpMethod="get")
