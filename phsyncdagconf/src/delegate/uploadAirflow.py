import json
import subprocess
import os

from util.AWS.ph_s3 import PhS3
from util.AWS.DynamoDB import DynamoDB
from util.AWS import define_value as dv

class Airflow:
    def __init__(self, **kwargs):
        self.phs3 = PhS3()
        self.dynamodb = DynamoDB()
        self.job_path_prefix = "/tmp/phjobs/"
        # 这个位置挂载 efs 下 /pharbers/projects
        self.operator_path = "/mnt/tmp/max/airflow/dags/"
        # self.efs_operator_path = "/mnt/tmp/max/airflow/dags/"


    def create_init(self, dag_conf, path=None):
        # lmd中默认创建到tmp下的phjobs /tmp/phjobs/

        dag_name = dag_conf.get("projectName") + \
                   "_" + dag_conf.get("dagName") + \
                   "_" + dag_conf.get("flowVersion")

        job_full_name = dag_conf.get("jobDisplayName")
        job_path = self.job_path_prefix + dag_name + "/" + job_full_name
        subprocess.call(["mkdir", "-p", job_path])
        subprocess.call(["touch", job_path + "/__init__.py"])

    def cerate_args_properties(self, dag_conf, path=None):
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

        job_full_name = dag_conf.get("jobDisplayName")
        job_path = self.job_path_prefix + dag_name + "/" + job_full_name

        f_lines = self.phs3.open_object_by_lines(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_PHMAIN_FILE_PY)
        with open(job_path + "/phmain.py", "w") as file:

            for line in f_lines:
                line = line + "\n"
                if line == "$alfred_debug_execute\n":
                    file.write("@click.command()\n")
                    for must in dv.PRESET_MUST_ARGS.split(","):
                        file.write("@click.option('--{}')\n".format(must.strip()))
                    # for input in json.loads(dag_conf.get("inputs")):
                    #     file.write("@click.option('--" + input.get("name") + "')\n")
                    # for output in json.loads(dag_conf.get("outputs")):
                    #     file.write("@click.option('--" + output.get("name") + "')\n")
                    file.write("""def debug_execute(**kwargs):
    try:
        logger = phs3logger(kwargs["job_id"], LOG_DEBUG_LEVEL)
        args = {"name": "$alfred_name"}
        inputs = [$alfred_inputs] 
        outputs = [$alfred_outputs_name]
        outputs_id = ["$alfred_output_id"]
        project_id = "$alfred_project_id"
        
        ph_conf = json.loads(kwargs.get("ph_conf"))
        logger.debug("打印ph_conf")
        logger.debug(ph_conf)
        logger.debug(type(ph_conf))
        args.update(ph_conf)
        result = exec_before(**args)

        args.update(result if isinstance(result, dict) else {})
        df_map = readClickhouse(inputs, args)
        args.update(df_map)
        result = execute(**args)

        args.update(result if isinstance(result, dict) else {})
        logger.debug("job脚本返回输出df")
        logger.debug(args)

        createOutputs(args, ph_conf, outputs, outputs_id, project_id, logger)

        for output in outputs:
            args.update({output: output})
        for input in inputs:
            args.update({input: input})
        result = exec_after(outputs=outputs, **args)

        return result
    except Exception as e:
        logger = phs3logger(kwargs["job_id"])
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
        raise e

"""
                               .replace('$alfred_outputs_name', ', '.join(['"'+output.get("name").lower()+'"' for output in json.loads(dag_conf.get("outputs"))])) \
                               .replace('$alfred_inputs', ', '.join(['"'+output.get("name").lower()+'"' for output in json.loads(dag_conf.get("inputs"))])) \
                               .replace('$alfred_outputs_id', ', '.join(['"'+output.get("id").lower()+'"' for output in json.loads(dag_conf.get("outputs"))])) \
                               .replace('$alfred_name', dag_conf.get("jobDisplayName"))
                               .replace('$alfred_project_id', dag_conf.get("projectId"))
                               )
                else:
                    file.write(line)

    def create_phjobs(self, dag_conf):
        # 通过 phcli 创建 phjobs 相关文件
        dag_name = dag_conf.get("projectName") + \
                   "_" + dag_conf.get("dagName") + \
                   "_" + dag_conf.get("flowVersion")

        job_full_name = dag_conf.get("jobDisplayName")
        job_path = self.job_path_prefix + dag_name + "/" + job_full_name

        # 2. /phjob.py file
        self.phs3.download(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_PHJOB_FILE_PY, job_path + "/phjob.py")
        with open(job_path + "/phjob.py", "a") as file:
            file.write("""def execute(**kwargs):\n""")

            file.write("""    logger = phs3logger(kwargs["job_id"], LOG_DEBUG_LEVEL)\n""")

            file.write("""
    result_path_prefix = kwargs["result_path_prefix"]
    spark = kwargs["spark"]()
    depends_path = kwargs["depends_path"]

    return {}
""")


    def upload_phjob_files(self, dag_conf):

        dag_name = dag_conf.get("projectName") + \
                   "_" + dag_conf.get("dagName") + \
                   "_" + dag_conf.get("flowVersion")
        operator_dir_path = self.job_path_prefix + dag_name + "/" + dag_conf.get("jobDisplayName")

        self.phs3.upload_dir(
            dir=operator_dir_path,
            bucket_name=dv.TEMPLATE_BUCKET,
            s3_dir=dv.CLI_VERSION + dv.DAGS_S3_PHJOBS_PATH + dag_name + "/" + dag_conf.get("jobDisplayName")
        )

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
            for link in links:
                w = open(operator_file_path, "a")
                f_lines = self.phs3.open_object_by_lines(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_PHGRAPHTEMP_FILE)
                for line in f_lines:
                    line = line + "\n"
                    w.write(
                        line.replace("$alfred_dag_owner", dag_conf.get("owner")) \
                            .replace("$alfred_email_on_failure", str("False")) \
                            .replace("$alfred_email_on_retry", str("False")) \
                            .replace("$alfred_email", str("['airflow@example.com']")) \
                            .replace("$alfred_retries", str(0)) \
                            .replace("$alfred_retry_delay", str("minutes=5")) \
                            .replace("$alfred_dag_id", str(dag_name)) \
                            .replace("$alfred_dag_tags", str("'default'")) \
                            .replace("$alfred_schedule_interval", str("None")) \
                            .replace("$alfred_description", str("A Max Auto Job Example")) \
                            .replace("$alfred_dag_timeout", str("3000.0")) \
                            .replace("$alfred_start_date", str(1))  \
                            .replace("$alfred_projectId", dag_conf.get("projectId"))
                    )

        def update_operator_file(operator_file_path, dag_name, links):

            w = open(operator_file_path, "a")
            jf = self.phs3.open_object_by_lines(dv.TEMPLATE_BUCKET, dv.CLI_VERSION + dv.TEMPLATE_PHDAGJOB_FILE)
            for line in jf:
                line = line + "\n"
                w.write(
                    line.replace("$alfred_jobs_dir", str(dag_name))
                        .replace("$alfred_name", str(dag_conf.get("jobDisplayName")))
                        .replace("$alfred_projectName", str(dag_conf.get("projectName")))
                        .replace("$alfred_jobShowName", str(dag_conf.get("jobShowName")))
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
            dag_name = res.get("Items")[0].get("projectName") +\
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


    def airflow(self, item_list):

        for item in item_list:
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

            # 创建上传job文件
            for dag_item in res.get("Items"):

                # 创建args_properties
                self.create_init(dag_item)
                self.cerate_args_properties(dag_item)
                self.create_phmain(dag_item)
                self.create_phjobs(dag_item)
                # 上传phjob文件
                self.upload_phjob_files(dag_item)

