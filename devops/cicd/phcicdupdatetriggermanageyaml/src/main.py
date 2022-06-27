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
                "version": "V001",
                "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
                "publisher": "赵浩博",
                "alias": "V001",
                "runtime": "dev",
                "trigger": {
                    "repo": "phlambda",
                    "branch": "feature/PBDP-3043-async-cicd-state-machine",
                    "prefix": "processor/sync/triggers/phsampletrigger",
                    "lmdName": "lmd-phsampletrigger-dev",
                    "sm": "processor/async/sample/sm.json",
                    "entry": {
                        "type": "Api GateWay",
                        "resource": "phsampletrigger"
                        "method": ["POST"]
                    },
                    "required": true
                },
                "apiGateWayArgs": {
                    "methods": ["POST"],
                    "PathPart": "phsampletrigger",
                    "LmdName": "lmd-phsampletrigger-dev",
                    "RestApiId": "",
                    "AuthorizerId": "",
                    "ParentId": ""
                }
            },
return:
    {
        "manageUrl": manageUrl,
        "stackName": stackName，
        "stackParameters": stackParameters 
    }
}
'''
manageTemplateS3Key = "ph-platform"
manageTemplateS3Path = "2020-11-11/cicd/template/manageTemplate.yaml"
apiTemplateS3Key = "ph-platform"
apiTemplateS3Path = "2020-11-11/cicd/template/apiResource.yaml"
resourcePathPrefix = "2020-11-11/cicd/"
manageUrlPrefix = "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/"
mangeLocalPath = "/tmp/manage.yaml"
apiResourceLocalPath = "/tmp/apiResource.yaml"


class Ref(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return u"!Ref " + self.value

    def deal(self):
        return u"!Ref " + self.value


class Sub(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return u"!Sub " + self.value

    def deal(self):
        return u"!Sub " + self.value


def ref_constructor(loader, node):
    value = loader.construct_scalar(node)
    value = Ref(value)
    return str(value)


def sub_constructor(loader, node):
    value = loader.construct_scalar(node)
    value = Sub(value)
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
    yaml.add_constructor(u'!Sub', sub_constructor)  # 添加代码来构造一个Sub对象
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


def insert_api_resource(methods, apiResourceResult):
    for method in methods:

    return 1


def lambda_handler(event, context):

    # 1 下载ApiResource文件、
    #   POST, GET, OPTIONS, DELETE, PATCH
    download_s3_file(apiTemplateS3Key, apiTemplateS3Path, apiTemplateS3Path)
    # 2 下载manage template文件
    if s3_file_exist("ph-platform", resourcePathPrefix + event["trigger"]["prefix"] + "/manage.yaml"):
        download_s3_file("ph-platform", resourcePathPrefix + event["trigger"]["prefix"] + "/manage.yaml",
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

    # 3 下载function的package.yaml文件 resourcePathPrefix + functionPath + "/package/package.yaml"
    lambdaArg = event["lambdaArgs"]
    functionPath = lambdaArg["parameters"]["FunctionPath"]
    functionName = lambdaArg["parameters"]["FunctionName"]
    package_s3_key = "ph-platform"
    package_s3_path = resourcePathPrefix + functionPath + "/package/package.yaml"
    package_local_path = "/tmp/" + functionName + "/package.yaml"
    # 从s3下载yaml文件
    download_s3_file(package_s3_key, package_s3_path, package_local_path)

    # 4 将 function package文件内容写入 manage中
    package_result = read_yaml_file(package_local_path)
    manage_result["Resources"][functionName] = package_result["Resources"]["ATTFFunction"]
    del manage_result["Resources"][functionName]["Metadata"]
    manage_result["Parameters"].update(package_result.get("Parameters", {}))
    manage_result["Outputs"].update(package_result.get("Outputs", {}))

    # 5 将 api 相关信息写入到 manage中
    apiResourceResult = read_yaml_file(apiResourceLocalPath)
    manage_result["Parameters"].update(apiResourceResult.get("Parameters", {}))
    manage_result["Outputs"].update(apiResourceResult.get("Outputs", {}))
    apiGateWayArgs = event["apiGateWayArgs"]
    methods = apiGateWayArgs["methods"]
    currentAPiResult = insert_api_resource(methods, apiResourceResult)
    manage_result["Resources"].update(currentAPiResult)
    # 6 上传manage文件 manageUrlPrefix + event["trigger"]["prefix"] + "/manage.yaml"

    return 1
