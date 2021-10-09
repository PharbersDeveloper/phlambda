import json
import time
import boto3


def lambda_handler(event, context):


    parameters = event['parameters']
    run_id = event['parameter']['run_id']
    dag_name = event['dag_parameters']['dag_name']
    job_full_name = event['dag_parameters']['job_full_name']
    owner = event.get('owner',"default_owner")
    use_merch_mapping = parameters.get('use_merch_mapping', None)

    if job_full_name == "data_model_shell_fragment":
        executorMemory = "4g"
        driverMemory = "1g"
    else:
        executorMemory = "1g"
        driverMemory = "1g"

    args = ["spark-submit",
            "--deploy-mode", "cluster",
            "--conf", "spark.driver.cores=1",
            "--conf", "spark.driver.memory=" + driverMemory,
            "--conf", "spark.executor.cores=1",
            "--conf", "spark.executor.memory=" + executorMemory,
            "--conf", "spark.executor.instances=1",
            "--conf", "spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
            "--conf", "spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
            "--jars", "s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/clickhouse-jdbc-0.2.4.jar,s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/guava-30.1.1-jre.jar",
            "--py-files",
            "s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-3.0.40-py3.8.egg,s3://ph-platform/2020-11-11/jobs/python/phcli/"+dag_name+"/"+job_full_name+"/phjob.py",
            "s3://ph-platform/2020-11-11/jobs/python/phcli/"+dag_name+"/"+job_full_name+"/phmain.py",
            "--owner", owner,
            "--dag_name", dag_name,
            "--run_id", run_id,
            "--job_full_name", job_full_name,
            "--job_id", "not_implementation"
            ]


    s3_client = boto3.client('s3')
    response = s3_client.get_object(
        Bucket="ph-platform",
        Key="2020-11-11/jobs/python/phcli/"+dag_name+"/"+job_full_name+"/args.properties"
    )

    args_str = response["Body"].read().decode()
    args_list = args_str.split("\n")
    deal_args_list=[]
    for arg in args_list:
        if "{{" or "}}" in arg:
            arg = arg.replace("}}", "} }").replace("{{", "{ {")
        deal_args_list.append(arg)

    # 将list转换成dict
    keys = []
    values = []
    for arg in deal_args_list:
        if deal_args_list.index(arg) % 2 == 0:
            keys.append(arg)
        elif deal_args_list.index(arg) % 2 == 1:
            values.append(arg)
    zip_args = zip(keys, values)
    dict_args = dict(zip_args)

    # 获取生成dict中的参数, 将传进来的dict进行替换
    for key in dict_args.keys():
        if key.lstrip('--') in parameters.keys():
            if type(parameters[key.lstrip('--')]) == dict:
                str_args = json.dumps(parameters[key.lstrip('--')], ensure_ascii=False)
                if "{{" or "}}" in str_args:
                    str_args = str_args.replace("}}", "} }").replace("{{", "{ {")
                dict_args[key] = str_args
            elif type(parameters[key.lstrip('--')]) == list:
                list_args = parameters[key.lstrip('--')]
                str_args = json.dumps(list_args)
                dict_args[key] = str_args
            else:
                dict_args[key] = parameters[key.lstrip('--')]

    dict_args.pop("--run_id",None)
    dict_args.pop("--dag_name",None)
    dict_args.pop("--owner",None)
    dict_args.pop("--job_full_name",None)
    dict_args.pop("--job_id",None)



    for key in dict_args.keys():
        args.append(key)
        args.append(dict_args[key])

    return {
        "use_merch_mapping": use_merch_mapping,
        "run_id" : run_id,
        "args": args
    }