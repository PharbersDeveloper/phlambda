import json
import boto3
import urllib.parse
import re

def lambda_handler(event, context):

    def get_s3_tag(key):
        s3_client = boto3.client("s3")
        response = s3_client.get_object_tagging(
            Bucket='ph-origin-files',
            Key=key,
        )
        tags={}
        for tag in response['TagSet']:
            tags[tag['Key']] = tag['Value']
        print("filename = " + key.split("/")[-1].strip(".xlsx"))
        return tags

    def create_g_mapper(mapper_list):

        g_mapper = []
        for mapper in mapper_list:
            mapper_tmp = {
                "dim": "0",
                "cat": "",
                "src": [],
                "des": ""
            }
            for key ,value in mapper.items():
                if value:
                    mapper_tmp["src"].append(value)
                    mapper_tmp["des"] = key
                    if value.lower() == key:
                        mapper_tmp["cat"] = "normal"
                    else:
                        mapper_tmp["cat"] = "rename"
                    g_mapper.append(mapper_tmp)
                else:
                    break

        return g_mapper

    def create_etl_parameters(tags, key,g_mapper):
        parameter = {}
        parameters = []
        parameter['table'] = key.split("/")[-2]
        parameter['in_path'] = "ph-origin-files" + "/" +"/" .join(key.split("/")[:-2]) + "/"
        parameter['out_path'] = "ph-platform/2020-11-11/etl/temporary_csv/"
        parameter['file'] = key.split("/")[-1]
        parameter['sheet'] = tags['sheet']
        parameter['header'] = "0"
        parameter['index_col'] = "0"
        parameter['provider'] = tags['provider']
        parameter['version'] = tags['version']
        parameter['owner'] = tags['owner']
        parameter['deal_content'] = 'false'
        parameter['type'] = "xlsx"
        parameter['g_partition'] = "provider, version， owner"
        parameter['g_filldefalut'] = "NONE"
        parameter['g_bucket'] = "NONE"

        table_name = "prod_standard_tmp"
        if g_mapper:
            parameter['g_mapper'] = g_mapper
            parameter['mapper_only'] = "true"
        else:
            parameter['mapper_only'] = "false"
        parameter['deal_content'] = "true"
        reg = ".xlsx"

        if tags['version'] == key.split("/")[-1].split(".")[0] + "_" + tags['sheet']:
            output = re.sub(reg, "", key.split("/")[-1] + "_" + tags['sheet'] + ".csv")
        else:
            output = re.sub(reg, "", key.split("/")[-1] + "_" + tags['sheet'] + "_" + tags['version'] + ".csv")
        p_input = "s3://" + "ph-platform" + "/2020-11-11/etl/temporary_csv/" + key.split("/")[-2] + "/" + output
        p_output = "s3://" + "ph-platform" + "/2020-11-11/etl/readable_files/" + table_name
        parameter['p_input'] = p_input
        parameter['p_output'] = p_output
        parameters.append(parameter)

        return parameters

    def get_clusterId():
        ssm_client = boto3.client('ssm')
        ssm_response = ssm_client.get_parameter(
            Name='cluster_id'
        )
        clusterId = ssm_response['Parameter']['Value']
        return clusterId

    def create_iterator():
        iterator = {
            "count": 2,
            "index": 0,
            "step": 1
        }

        return iterator

    def start_execution(parameters):
        machine_input={}
        machine_input['clusterId'] = get_clusterId()
        machine_input['iterator'] = create_iterator()
        machine_input['parameters'] = parameters
        step_client = boto3.client('stepfunctions')
        print(machine_input)
        # 启动状态机
        response = step_client.start_execution(
            stateMachineArn='arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:ETL_Iterator',
            input=json.dumps(machine_input,ensure_ascii=False)
        )
        return response['executionArn']

    def send_msg_to_lmd(tags, executionArn):
        executionId = tags['executionId']
        executionArn = executionArn
        stateMachineArn = "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:ETL_Iterator"
        Message = {
            "executionId": executionId,
            "executionArn": executionArn,
            "stateMachineArn": stateMachineArn
        }
        Message_str = json.dumps(Message, ensure_ascii=False)
        etlsfnindex = {
            "Records": [
                {
                    "Sns": {
                        "Subject": "functionindex",
                        "Message": Message_str,
                        "MessageAttributes": {
                            "action": {
                                "Type": "String",
                                "Value": "update"
                            },
                            "type": {
                                "Type": "String",
                                "Value": "execution"
                            }
                        }
                    }
                }
            ]
        }
        lmd_client = boto3.client("lambda")
        response = lmd_client.invoke(
            FunctionName='phsfnindex',
            Payload=json.dumps(etlsfnindex).encode()
        )


    print(event)
    # 获取S3文件的具体路径
    key = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])

    # 1.根据key获取指定文件的tags
    tags = get_s3_tag(key)

    # 获取mapper_list 创建g_mapper
    mapper_list = tags["mapper_list"]
    g_mapper = create_g_mapper(mapper_list)

    # 2.根据key和tags创建运行stepfunction的parameters
    parameters = create_etl_parameters(tags, key, g_mapper)

    # 3.传入parameters启动stepfuntion返回 executionArn
    executionArn = start_execution(parameters)

    # 启动钱ETL

    # 4.将指定参数提供给lmd写入数据库
    send_msg_to_lmd(tags, executionArn)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
        "body": json.dumps({
            "executionArn": executionArn

        })
    }