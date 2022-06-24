import yaml
import os
import boto3

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
cfn_client = boto3.client('cloudformation')
'''
将错误提取出来写入到notification中
args:
    event = {   
                "version": "20220622",
                "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
                "publisher": "赵浩博",
                "alias": "Current",
                "runtime": "dev",
                "lambdaArgs": [
                    {   
                        "stackName": "functionName"
                        "functionPath": "",
                        "functionPrefixPath": "",
                        "buildSpec": "",
                        "codebuildCfn": "",
                        "functionName": "",
                        "branchName": "",
                        "repoName": "",
                        "alias": "",
                        "gitCommit": "",
                        "gitUrl": ""
                    }, {...}
                ],
                "stepFunctionArgs": {
                    "stateMachineName": "functionName + codebuild",
                    "submitOwner": "",
                    "s3Bucket": "",
                    "s3TemplateKey": ""
                }
            },
return:
    {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
    }
}
'''
manageTemplateS3Key = "ph-platform"
manageTemplateS3Path = "2020-11-11/cicd/template/manageTemplate.yaml"
sfnTemplateS3Key = "ph-platform"
sfnTemplateS3Path = "2020-11-11/cicd/template/sfnTemplate.yaml"
resourcePathPrefix = "2020-11-11/cicd/"
manageUrlPrefix = "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/"
mangeLocalPath = "/tmp/manage.yaml"
sfnLocalPath = "/tmp/sfnTemplate.yaml"


class Ref(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return u"!Ref " + self.value

    def deal(self):
        return u"!Ref " + self.value


def ref_constructor(loader, node):
    value = loader.construct_scalar(node)
    value = Ref(value)
    return str(value)


def upload_s3_file(bucket_name, object_name, file):
    s3_client.upload_file(
        Bucket=bucket_name,
        Key=object_name,
        Filename=file
    )


def download_s3_file(s3_key, s3_path, local_path):

    local_dir_path = "/".join(local_path.split("/")[0:-1])
    if not os.path.exists(local_dir_path):
        os.makedirs(local_dir_path)

    with open(local_path, 'wb') as data:
        s3_client.download_fileobj(s3_key, s3_path, data)


def read_yaml_file(file_path):

    yaml.add_constructor(u'!Ref', ref_constructor)  # 添加代码来构造一个Ref对象
    with open(file_path, encoding='utf-8') as file:
        result = yaml.load(file.read(), Loader=yaml.FullLoader)
    return result


def write_yaml_file(result, file_path):

    f = open(file_path, "w")
    for line in yaml.dump(result):
        f.write(line.replace("'", ""))
    f.close()


def s3_file_exist(s3_key, s3_path):
    result = False
    bucket = s3_resource.Bucket(s3_key)
    for obj in bucket.objects.filter(Prefix=s3_path):
        if obj.key == s3_path:
            result = True
    return result


def lambda_handler(event, context):
    print(event)
    # 从s3下载sfn template文件
    download_s3_file(sfnTemplateS3Key, sfnTemplateS3Path, sfnLocalPath)
    # 判断manage.yaml文件是否存在 存在则下载 对此文件进行更改
    if s3_file_exist("ph-platform", resourcePathPrefix + event["processor"]["prefix"] + "/manage.yaml"):
        download_s3_file("ph-platform", resourcePathPrefix + event["processor"]["prefix"] + "/manage.yaml",
                         mangeLocalPath)
        manage_result = read_yaml_file(mangeLocalPath)
    else:
        # 如果不存在 从s3下载manage template文件
        download_s3_file(manageTemplateS3Key, manageTemplateS3Path, mangeLocalPath)
        # 读取manage.yaml文件内容
        manage_result = read_yaml_file(mangeLocalPath)
        manage_result["Resources"] = {}
        manage_result["Parameters"] = {}
        manage_result["Outputs"] = {}
    print(manage_result)
    # 将sfnTemplate.yaml文件写入到 manage文件中
    sfnTemplateResult = read_yaml_file(sfnLocalPath)
    print(sfnTemplateResult)
    manage_result["Resources"].update(sfnTemplateResult.get("Resources", {}))
    manage_result["Parameters"].update(sfnTemplateResult.get("Parameters", {}))
    manage_result["Outputs"].update(sfnTemplateResult.get("Outputs", {}))
    print(manage_result)
    # 获取每个function package.yaml的内容
    # 获取functionPath拼接出s3路径
    for lambdaArg in event["lambdaArgs"]:
        functionPath = lambdaArg["functionPath"]
        functionName = lambdaArg["functionName"]
        package_s3_key = "ph-platform"
        package_s3_path = resourcePathPrefix + functionPath + "/package/package.yaml"
        package_local_path = "/tmp/" + lambdaArg["functionName"] + "/package.yaml"
        # 从s3下载yaml文件
        download_s3_file(package_s3_key, package_s3_path, package_local_path)
        # 写入到manage
        package_result = read_yaml_file(package_local_path)
        manage_result["Resources"][functionName] = package_result["Resources"]["ATTFFunction"]
        del manage_result["Resources"][functionName]["Metadata"]
        manage_result["Parameters"].update(package_result.get("Parameters", {}))
        manage_result["Outputs"].update(package_result.get("Outputs", {}))

    print(manage_result)
    write_yaml_file(manage_result, mangeLocalPath)
    upload_s3_file(
        bucket_name=manageTemplateS3Key,
        object_name=resourcePathPrefix + event["processor"]["prefix"] + "/manage.yaml",
        file=mangeLocalPath
    )
    manageUrl = manageUrlPrefix + event["processor"]["prefix"] + "/manage.yaml"
    print(manageUrl)
    # 创建resource cfn
    stackName = event["processor"]["stateMachineName"] + "-resource"

    return {
        "manageUrl": manageUrl,
        "stackName": stackName
    }
