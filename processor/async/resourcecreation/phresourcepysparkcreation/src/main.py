import json
import os
import subprocess
from util.AWS import define_value as dv
from util.AWS.ph_s3 import PhS3
from handler.GenerateInvoker import GenerateInvoker


'''
创建pyspark
args = {
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "dagName": "String",
    "owner": "String",
    "projectName": "String",
    "scripts": {
        "id": "String",
        "runtime": "String",
        "name": "String",
        "flowVersion": "developer",
        "inputs": "[]",
        "output": "{}"
    }
}
'''
phs3 = PhS3()
job_path_prefix = "/tmp/phjobs/"

def create_phjobs(args):
    runtime = args["script"].get("runtime")
    if runtime == "prepare":
        runtime = "pyspark"

    # 通过 phcli 创建 phjobs 相关文件
    dag_name = args.get("projectName") + \
               "_" + args.get("dagName") + \
               "_" + args["script"].get("flowVersion")

    job_full_name = dag_name + "_" + args["script"].get("name")
    job_path = job_path_prefix + dag_name + "/" + job_full_name
    phjob_exist = False
    job_name = "phjob"

    # 如果是script脚本先判断文件是否在s3存在 如果存在不生成phjob文件
    phjob_exist = phs3.file_exist(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.DAGS_S3_PHJOBS_PATH + dag_name + "/" + job_full_name + "/" + "phjob.py")
    print("Tobeey =======>>>>>>>>")
    print("判断s3是否存在")
    print(phjob_exist)
    print("Tobeey =======>>>>>>>>")
    operator_parameters = [{"type": "Script"}]
    if not phjob_exist:
        # 2. /phjob.py file
        phs3.download(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_PHJOB_FILE_PY, job_path + "/" + "phjob.py")
        operator_code = GenerateInvoker().execute(operator_parameters, runtime)
        with open(job_path + "/" + "phjob.py", "a") as file:
            file.write("""def execute(**kwargs):\n""")
            file.write(operator_code)

    for key in os.listdir(job_path):
        print(key)

def create_phmain(args, path=None):
    if not path:
        dag_name = args.get("projectName") + \
                   "_" + args.get("dagName") + \
                   "_" + args["script"].get("flowVersion")

    job_full_name = dag_name + "_" + args["script"].get("name")

    job_path = job_path_prefix + dag_name + "/" + job_full_name
    if os.path.exists(job_path + "/phmain.py"):
        os.system("rm " + job_path + "/phmain.py")

    subprocess.call(["mkdir", "-p", job_path])

    f_lines = phs3.open_object_by_lines(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_PHMAIN_FILE_PY)

    def write_python():
        with open(job_path + "/phmain.py", "w") as file:
            for line in f_lines:
                line = line + "\n"
                if line == "$alfred_debug_execute\n":
                    file.write("@click.command()\n")
                    for must in dv.PRESET_MUST_ARGS.split(","):
                        file.write("@click.option('--{}')\n".format(must.strip()))
                    file.write("""def debug_execute(**kwargs):
    try:
        logger = phs3logger("emr_log", LOG_DEBUG_LEVEL)
        args = {"name": "$alfred_name"}
        inputs = $alfred_inputs
        output = "$alfred_output_name"
        project_id = "$alfred_project_id"
        project_name = "$alfred_project_name"
        runtime = "$alfred_runtime"
        
        project_ip = kwargs.get("project_ip")
        ph_conf = json.loads(kwargs.get("ph_conf", {}))
        user_conf = ph_conf.get("userConf", {})
        ds_conf = ph_conf.get("datasets", {})
        logger.debug("打印 user_conf")
        logger.debug(user_conf)
        logger.debug(type(user_conf))
        logger.debug("打印 ds_conf")
        logger.debug(ds_conf)
        logger.debug(type(ds_conf))
        args.update(user_conf)
        args.update({"ds_conf": ds_conf})
    
        args.update(kwargs)
        output_version =  args.get("run_id") + "_" + ph_conf.get("showName")

        df_map = create_input_df(runtime, inputs, args, project_id, project_name, output_version, logger)
        args.update(df_map)
        result = execute(**args)

        args.update(result if isinstance(result, dict) else {})
        logger.debug("job脚本返回输出df")
        logger.debug(args)
        
        createOutputs(runtime, args, ph_conf, output, project_ip, project_id, project_name, output_version, logger)

        return result
    except Exception as e:
        logger = phs3logger("emr_log")
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
        raise e

"""
                               .replace('$alfred_output_name', args["script"].get("output"))
                               .replace('$alfred_inputs', args["script"].get("inputs"))
                               .replace('$alfred_name', job_full_name)
                               .replace('$alfred_project_id', args["projectId"])
                               .replace('$alfred_project_name', args["projectId"])
                               .replace('$alfred_runtime', args["script"].get("runtime"))
                               )
                else:
                    file.write(line)

    for key in os.listdir(job_path):
        print(key)
    write_python()


def create_traceId(args):

    traceId = args.get("traceId")
    dag_name = args.get("projectName") + \
               "_" + args.get("dagName") + \
               "_" + args["script"].get("flowVersion")

    job_full_name = dag_name + "_" + args["script"].get("name")
    job_path = job_path_prefix + dag_name + "/" + job_full_name + "/"
    subprocess.call(["touch", job_path + traceId])


def upload_phjob_files(args):

    dag_name = args.get("projectName") + \
               "_" + args.get("dagName") + \
               "_" + args["script"].get("flowVersion")

    job_full_name = dag_name + "_" + args["script"].get("name")

    def upload_job(operator_dir_path, dag_name):
        phs3.upload_dir(
            dir=operator_dir_path,
            bucket_name=dv.TEMPLATE_BUCKET,
            s3_dir=dv.CLI_VERSION + dv.DAGS_S3_PHJOBS_PATH + dag_name + "/" + job_full_name
        )
    operator_dir_path = job_path_prefix + dag_name + "/" + job_full_name
    # runtime = dag_conf.get("runtime")
    upload_job(operator_dir_path, dag_name)


def lambda_handler(event, context):
    print(event)

    if event["script"].get("name"):
        # 创建pyspark的流程
        create_phmain(event)
        print("创建phmain成功")
        create_phjobs(event)
        print("创建phjob成功")
        create_traceId(event)
        print("traceId文件创建成功")
        upload_phjob_files(event)
        print("上传phjob文件成功")

    result = event["script"]
    
    return result
