import json
import subprocess
import os

from delegate.createDagByItem.command import Command
from util.AWS.ph_s3 import PhS3
from util.AWS.DynamoDB import DynamoDB
from util.AWS import define_value as dv
from handler.GenerateInvoker import GenerateInvoker
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL

default_args = {
    "python3_phmain": dv.TEMPLATE_PHMAIN_FILE_PY,
    "python3_phgraphtemp": dv.TEMPLATE_PHGRAPHTEMP_FILE,
    "python3_phdagjob": dv.TEMPLATE_PHDAGJOB_FILE,
    "prepare_phmain": dv.TEMPLATE_PHMAIN_FILE_PY,
    "prepare_phgraphtemp": dv.TEMPLATE_PHGRAPHTEMP_FILE,
    "prepare_phdagjob": dv.TEMPLATE_PHDAGJOB_FILE,
    "pyspark_phmain": dv.TEMPLATE_PHMAIN_FILE_PY,
    "pyspark_phgraphtemp": dv.TEMPLATE_PHGRAPHTEMP_FILE,
    "pyspark_phdagjob": dv.TEMPLATE_PHDAGJOB_FILE,
    "r_phmain": dv.TEMPLATE_PHMAIN_FILE_R,
    "r_phgraphtemp": dv.TEMPLATE_PHGRAPHTEMP_FILE,
    "r_phdagjob": dv.TEMPLATE_PHDAGJOB_FILE,
    "sparkr_phmain": dv.TEMPLATE_PHMAIN_FILE_R,
    "sparkr_phgraphtemp": dv.TEMPLATE_PHGRAPHTEMP_FILE,
    "sparkr_phdagjob": dv.TEMPLATE_PHDAGJOB_FILE
}

# 最终生成模板的重构为 外观 -> 构造 -> 工厂/策略
# 外观统一接口 构造按照顺序产出结构 工厂/策略拿到结构进行核心代码拼装

class CommandUploadAirflow(Command):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.phs3 = PhS3()
        self.dynamodb = DynamoDB()
        self.job_path_prefix = "/tmp/phjobs/"
        # self.job_path_prefix = "/Users/qianpeng/GitHub/phlambda/phsyncdagconf/src/phjobs/"
        # 这个位置挂载 efs 下 /pharbers/projects
        self.operator_path = "/mnt/tmp/" + json.loads(self.dag_item["message"]).get("projectId") + "/airflow/dags/"
        # self.operator_path = "/Users/qianpeng/GitHub/phlambda/phsyncdagconf/src/dags/"
        self.efs_operator_path = "/mnt/tmp/max/airflow/dags/"
        self.logger = PhLogging().phLogger("upload_airflow_file", LOG_DEBUG_LEVEL)

    def create_init(self, dag_conf, path=None):
        # lmd中默认创建到tmp下的phjobs /tmp/phjobs/

        dag_name = dag_conf.get("projectName") + \
                   "_" + dag_conf.get("dagName") + \
                   "_" + dag_conf.get("flowVersion")

        job_full_name = dag_conf.get("jobDisplayName")
        job_path = self.job_path_prefix + dag_name + "/" + job_full_name
        subprocess.call(["mkdir", "-p", job_path])
        subprocess.call(["touch", job_path + "/__init__.py"])

    def create_args_properties(self, dag_conf, path=None):
        # if not path:
        #     path = self.job_path + "/arg.properties"
        # subprocess.call(["touch", path])
        dag_name = dag_conf.get("projectName") + \
                   "_" + dag_conf.get("dagName") + \
                   "_" + dag_conf.get("flowVersion")

        job_full_name = dag_conf.get("jobDisplayName")
        job_path = self.job_path_prefix + dag_name + "/" + job_full_name


        subprocess.call(["touch", job_path + "/args.properties"])
        with open(job_path + "/args.properties", "w") as file:
            # 遍历 dag_conf input name 作为 key id 作为 value
            for input in json.loads(dag_conf.get("inputs")):
                file.write("--{}".format(input.get("name")) + "\n")
                file.write(input.get("id") + "\n")

            for output in json.loads(dag_conf.get("outputs")):
                file.write("--{}".format(output.get("name")) + "\n")
                file.write(output.get("id") + "\n")

    def create_phmain(self, dag_conf, path=None):
        if not path:
            dag_name = dag_conf.get("projectName") + \
                       "_" + dag_conf.get("dagName") + \
                       "_" + dag_conf.get("flowVersion")

        runtime = dag_conf.get("runtime")

        job_full_name = dag_conf.get("jobDisplayName")
        job_path = self.job_path_prefix + dag_name + "/" + job_full_name
        f_lines = self.phs3.open_object_by_lines(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + default_args.get(runtime+"_phmain"))

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
        inputs = [$alfred_inputs] 
        outputs = [$alfred_outputs_name]
        outputs_id = [$alfred_outputs_id]
        project_id = "$alfred_project_id"
        project_name = "$alfred_project_name"
        runtime = "$alfred_runtime"
        
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
        
        createOutputs(runtime, args, ph_conf, outputs, outputs_id, project_id, project_name, output_version, logger)

        return result
    except Exception as e:
        logger = phs3logger(kwargs["job_id"])
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
        raise e

"""
                                   .replace('$alfred_outputs_name', ', '.join(['"'+output.get("name")+'"' for output in json.loads(dag_conf.get("outputs"))])) \
                                   .replace('$alfred_inputs', ', '.join(['"'+input.get("name")+'"' for input in json.loads(dag_conf.get("inputs"))])) \
                                   .replace('$alfred_outputs_id', ', '.join(['"'+output.get("id")+'"' for output in json.loads(dag_conf.get("outputs"))])) \
                                   .replace('$alfred_name', dag_conf.get("jobDisplayName"))
                                   .replace('$alfred_project_id', dag_conf.get("projectId"))
                                   .replace('$alfred_project_name', dag_conf.get("dagName"))
                                   .replace('$alfred_runtime', dag_conf.get("runtime"))
                                   )
                    else:
                        file.write(line)

        def write_r():
            with open(job_path + "/phmain.R", "w") as file:
                for line in f_lines:
                    line = line + "\n"
                    if line == "$alfred_debug_execute\n":
                        file.write(f"""
args <- list(name="{dag_conf.get("jobDisplayName")}")

inputs <- list({', '.join(['"'+input.get("name")+'"' for input in json.loads(dag_conf.get("inputs"))])})
outputs <- list({', '.join(['"'+output.get("name")+'"' for output in json.loads(dag_conf.get("outputs"))])})

outputs_id <- list({', '.join(['"'+output.get("id")+'"' for output in json.loads(dag_conf.get("outputs"))])})
project_id <- "{dag_conf.get("projectId")}"
project_name <- "{dag_conf.get("dagName")}"
runtime <- "{runtime}"

ph_conf <- fromJSON(input_args$ph_conf, simplifyVector=FALSE)

user_conf <- ph_conf$userConf

ds_conf <- as.list(ph_conf$datasets)

args <- c(args, user_conf)
args[["ds_conf"]] <- ds_conf
args <- c(args, input_args)

output_version <- paste(args$run_id, "_", ph_conf$showName, sep="")

df_map <- create_input_df(runtime, inputs, args, project_id, project_name, output_version)

args <- c(args, df_map)

result <- exec(args)

args <- c(args, result)

create_outputs(runtime, args, ph_conf, outputs, outputs_id, project_id, project_name, output_version)
                        """)
                    else:
                        file.write(line)

        choose_main = {
            "python3": write_python,
            "pyspark": write_python,
            "r": write_r,
            "sparkr": write_r,
            "prepare": write_python
        }

        choose_main[runtime]()


    def edit_prepare_phjob(self, message):
        jobDisplayName = message.get("jobDisplayName")
        jobName = message.get("jobName")
        operatorParameters = message.get("operatorParameters")
        projectName = message.get("projectName")
        flowVersion = message.get("flowVersion")
        projectId = message.get("projectId")

        dag_name = projectName + \
                   "_" + projectName + \
                   "_" + flowVersion

        job_full_name = jobDisplayName

        job_path = self.job_path_prefix + dag_name + "/" + job_full_name
        print(operatorParameters)

        subprocess.call(["mkdir", "-p", job_path])

        # 2. /phjob.py file
        self.phs3.download(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_PHJOB_FILE_PY, job_path + "/phjob.py")
        operator_code = GenerateInvoker().execute(operatorParameters, "prepare")
        with open(job_path + "/phjob.py", "a") as file:
            # file.write("""def execute(**kwargs):\n""")
            file.write("")
            file.write(operator_code)

        # 创建完成后将脚本上传到s3
        self.phs3.upload(
            file=job_path + "/phjob.py",
            bucket_name=dv.TEMPLATE_BUCKET,
            object_name=dv.CLI_VERSION + dv.DAGS_S3_PHJOBS_PATH + dag_name + "/" + job_full_name + "/phjob.py"
        )

        # 查询 dag_conf item 修改 operatorParameters 字段
        data = {}
        data.update({"table_name": "dagconf"})
        key = {
            "projectId": projectId,
            "jobName": jobName
        }
        data.update({"key": key})
        res = self.dynamodb.getItem(data)

        item = res["Item"]
        item.update({"operatorParameters": json.dumps(operatorParameters, ensure_ascii=False)})
        edit_data = {
            "table_name": "dagconf",
            "item": item
        }
        self.dynamodb.putData(edit_data)

    def create_phjobs(self, dag_conf):
        runtime = dag_conf.get("runtime")

        # 通过 phcli 创建 phjobs 相关文件
        dag_name = dag_conf.get("projectName") + \
                   "_" + dag_conf.get("dagName") + \
                   "_" + dag_conf.get("flowVersion")

        job_full_name = dag_conf.get("jobDisplayName")
        job_path = self.job_path_prefix + dag_name + "/" + job_full_name
        operator_parameters = json.loads(dag_conf.get("operatorParameters"))

        phjob_exist = False

        job_name = "phjob"

        def write_r():
            return job_name + ".R"

        def write_python():
            return job_name + ".py"

        job_head_temps = {
            "python3": dv.TEMPLATE_PHJOB_FILE_PY,
            "pyspark": dv.TEMPLATE_PHJOB_FILE_PY,
            "r": dv.TEMPLATE_PHJOB_FILE_R,
            "sparkr": dv.TEMPLATE_PHJOB_FILE_R,
            "prepare": dv.TEMPLATE_PHJOB_FILE_PY
        }

        choose_job = {
            "python3": write_python,
            "pyspark": write_python,
            "r": write_r,
            "sparkr": write_r,
            "prepare": write_python
        }

        choose_job_head = {
            "python3": """def execute(**kwargs):\n""",
            "pyspark": """def execute(**kwargs):\n""",
            "prepare": "",
            "r": "",
            "sparkr": ""
        }

        # 如果是script脚本先判断文件是否在s3存在 如果存在不生成phjob文件
        if "Script" in list(map(lambda item: item["type"], operator_parameters)):
            phjob_exist = self.phs3.file_exist(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.DAGS_S3_PHJOBS_PATH + dag_name + "/" + job_full_name + "/" + choose_job[runtime]())
        print("Tobeey =======>>>>>>>>")
        print("判断s3是否存在")
        print(operator_parameters)
        print(dag_name + "/" + job_full_name + "/" + choose_job[runtime]())
        print(phjob_exist)
        print("Tobeey =======>>>>>>>>")
        if not phjob_exist:
            # 2. /phjob.py file
            self.phs3.download(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + job_head_temps[runtime], job_path + "/" + choose_job[runtime]())
            operator_code = GenerateInvoker().execute(operator_parameters, runtime)
            with open(job_path + "/" + choose_job[runtime](), "a") as file:
                file.write(choose_job_head[runtime])
                file.write(operator_code)

    def upload_phjob_files(self, dag_conf):

        def upload_job(operator_dir_path, dag_name):
            self.phs3.upload_dir(
                dir=operator_dir_path,
                bucket_name=dv.TEMPLATE_BUCKET,
                s3_dir=dv.CLI_VERSION + dv.DAGS_S3_PHJOBS_PATH + dag_name + "/" + dag_conf.get("jobDisplayName")
            )

        dag_name = dag_conf.get("projectName") + \
                   "_" + dag_conf.get("dagName") + \
                   "_" + dag_conf.get("flowVersion")
        operator_dir_path = self.job_path_prefix + dag_name + "/" + dag_conf.get("jobDisplayName")
        # runtime = dag_conf.get("runtime")
        upload_job(operator_dir_path, dag_name)

    def airflow_operator_file(self, dag_conf):

        def create_airflow_link():
            links = []
            if json.loads(dag_conf.get("targetJobId")):
                for targetJobId in json.loads(dag_conf.get("targetJobId")):
                    flowVersion = dag_conf.get("flowVersion")

                    # 通过targetJobId 查询 jobDisplayName
                    data = {
                        "table_name": "dagconf",
                        "partition_key": "projectId",
                        "partition_value": dag_conf.get("projectId"),
                        "sort_key": "jobName",
                        "sort_value": flowVersion + "_" + targetJobId + "_" + dag_conf.get("projectName")
                    }
                    res = self.dynamodb.queryTableBeginWith(data)
                    if res.get("Items"):
                        targetJobName = res["Items"][0].get("jobDisplayName")
                        link = dag_conf.get("jobDisplayName") + " >> " + targetJobName
                    else:
                        link = dag_conf.get("jobDisplayName")
                    links.append(link)
            else:
                link = dag_conf.get("jobDisplayName")
                links.append(link)

            return links

        def create_operator_file(operator_dir_path, dag_name, links):
            # for link in links:
            w = open(operator_file_path, "a")
            self.logger.debug("脚本运行时")
            self.logger.debug(dag_conf)
            runtime = dag_conf.get("runtime")
            self.logger.debug(runtime)
            self.logger.debug(default_args.get(runtime + "_phgraphtemp"))
            f_lines = self.phs3.open_object_by_lines(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + default_args.get(runtime + "_phgraphtemp"))
            for line in f_lines:
                line = line + "\n"
                w.write(
                    line.replace("$alfred_dag_owner", dag_conf.get("owner")) \
                        .replace("$alfred_email_on_failure", str("False")) \
                        .replace("$alfred_dag_showName", dag_conf.get("showName", "default_showName")) \
                        .replace("$alfred_email_on_retry", str("False")) \
                        .replace("$alfred_email", str("['airflow@example.com']")) \
                        .replace("$alfred_retries", str(0)) \
                        .replace("$alfred_retry_delay", str("minutes=5")) \
                        .replace("$alfred_dag_id", str(dag_name)) \
                        .replace("$alfred_dag_tags", str("'default'")) \
                        .replace("$alfred_schedule_interval", str("None")) \
                        .replace("$alfred_description", str("A Max Auto Job Example")) \
                        .replace("$alfred_dag_timeout", str("3000.0")) \
                        .replace("$alfred_start_date", str(1)) \
                        .replace("$alfred_projectId", dag_conf.get("projectId"))
                )

        def update_operator_file(operator_file_path, dag_name, links):

            runtime = dag_conf.get("runtime")
            output_id = json.loads(dag_conf.get("outputs"))[0].get("id")
            w = open(operator_file_path, "a")
            jf = self.phs3.open_object_by_lines(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + default_args.get(runtime + "_phdagjob"))
            for line in jf:
                line = line + "\n"
                w.write(
                    line.replace("$alfred_jobs_dir", str(dag_name))
                        .replace("$alfred_name", str(dag_conf.get("jobDisplayName")))
                        .replace("$alfred_projectName", str(dag_conf.get("projectName")))
                        .replace("$alfred_jobShowName", str(dag_conf.get("jobShowName")))
                        .replace("$alfred_runtime", runtime)
                        .replace("$alfred_output_id", output_id)
                )
            w.close()


        # 判断dag的operator是否存在 存在则直接添加
        # 如果没有则根据模板创建
        dag_name = dag_conf.get("projectName") + \
                   "_" + dag_conf.get("dagName") + \
                   "_" + dag_conf.get("flowVersion")
        operator_file_name = "ph_dag_" + dag_name + ".py"
        operator_dir_path = self.operator_path
        operator_file_path = operator_dir_path + operator_file_name
        if os.path.exists(operator_file_path):
            links = create_airflow_link()
            update_operator_file(operator_file_path, dag_name, links)
        else:
            links = create_airflow_link()
            create_operator_file(operator_dir_path, dag_name, links)
            update_operator_file(operator_file_path, dag_name, links)
        return links

    def update_operator_link(self, operator_file_path, flow_links):

        for link in flow_links:
            w = open(operator_file_path, "a")
            w.write(link.replace('.', '_'))
            w.write("\n")
            w.close()

    def airflow_operator_exec(self, item, res):

        if item.get("jobCat") == "dag_refresh":
            dag_name = res.get("Items")[0].get("projectName") + \
                       "_" + res.get("Items")[0].get("dagName") + \
                       "_" + res.get("Items")[0].get("flowVersion")
        else:
            dag_name = json.loads(item["message"]).get("projectName") + \
                       "_" + json.loads(item["message"]).get("dagName") + \
                       "_" + json.loads(item["message"]).get("flowVersion")

        operator_file_name = "ph_dag_" + dag_name + ".py"

        operator_dir_path = self.operator_path
        operator_file_path = operator_dir_path + operator_file_name

        if os.path.exists(operator_file_path):
            os.system("rm " + operator_file_path)
        # 创建airflow_operator 先写入没有targetJobId

        flow_links = []
        for dag_item in res.get("Items"):
            if not eval(dag_item.get("targetJobId")):
                link = self.airflow_operator_file(dag_item)
                flow_links.extend(link)
        # # 更新airflow_operator 写入有targetJobId
        for dag_item in res.get("Items"):
            if eval(dag_item.get("targetJobId")):
                link = self.airflow_operator_file(dag_item)
                flow_links.extend(link)
        self.update_operator_link(operator_file_path, flow_links)

    def airflow(self, item):
        # 获取所有的item 进行创建airflow
        projectId = json.loads(item["message"]).get("projectId")
        flowVersion = json.loads(item["message"]).get("flowVersion")
        data = {}
        data.update({"table_name": "dagconf"})
        data.update({"partition_key": "projectId"})
        data.update({"partition_value": projectId})
        data.update({"sort_key": "jobName"})
        data.update({"sort_value": flowVersion})
        res = self.dynamodb.queryTableBeginWith(data)
        # 创建airflow_operator
        self.airflow_operator_exec(item, res)
        dag_name = json.loads(item["message"]).get("projectName") + \
                   "_" + json.loads(item["message"]).get("dagName") + \
                   "_" + json.loads(item["message"]).get("flowVersion")


        os.system("rm -rf " + self.job_path_prefix + "/" + dag_name)
        # 创建上传job文件
        for dag_item in res.get("Items"):
            # 创建args_properties
            self.create_init(dag_item)
            self.create_args_properties(dag_item)
            self.create_phmain(dag_item)
            self.create_phjobs(dag_item)
            # 上传phjob文件
            self.upload_phjob_files(dag_item)

    def run(self):

        self.logger.debug("运行创建airflow文件命令")
        self.logger.debug(self.dag_item)
        self.airflow(self.dag_item)

