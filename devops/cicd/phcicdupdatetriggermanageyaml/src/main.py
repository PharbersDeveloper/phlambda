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
                "publisher": "赵浩博",
                "alias": "V001",
                "runtime": "dev",
                "trigger": {
                    "repo": "phlambda",
                    "branch": "feature/PBDP-3043-async-cicd-state-machine",
                    "prefix": "processor/sync/triggers",
                    "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
                    "functionName": "phsampletrigger",
                    "sm": "processor/async/sample/sm.json",
                    "entry": {
                        "type": "Api GateWay",
                        "resource": "phsampletrigger",
                        "method": ["POST"]
                    },
                    "required": true
                },
                "apiGateWayArgs": {
                    "methods": ["POST"],
                    "PathPart": "phsampletrigger",
                    "LmdName": "lmd-phsampletrigger-dev",
                    "RestApiId": "ksakt69kwb",
                    "AuthorizerId": "4xyac0",
                    "ParentId": "iiqaf4p618"
                }
            }
return:
    {
        "manageUrl": manageUrl,
        "stackName": stackName，
        "stackParameters": stackParameters 
    }
}
'''
manageTemplateS3Key = "ph-platform"
manageTemplateS3Path = "2020-11-11/cicd/template/manageApiTemplate.yaml"
apiTemplateS3Key = "ph-platform"
apiTemplateS3PathPrefix = "2020-11-11/cicd/template/"
resourcePathPrefix = "2020-11-11/cicd/"
manageUrlPrefix = "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/"
mangeLocalPath = "/tmp/manage.yaml"
apiResourceLocalPathPrefix = "/tmp/cicd/apiTmp/"


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
    # print(yaml.dump(result))
    for line in yaml.dump(result):
        f.write(line.replace("'", ""))
    f.close()


def write_api_resource(apiGateWayArgs, version):
    methods = apiGateWayArgs["methods"]
    print(type(methods))
    methods.insert(0, "Init")

    f2 = open(mangeLocalPath, "a+")
    for method in methods:
        download_s3_file(
            apiTemplateS3Key,
            apiTemplateS3PathPrefix + "api" + method.upper() + "Resource.yaml",
            apiResourceLocalPathPrefix + "api" + method.upper() + "Resource.yaml")
        f1 = open(apiResourceLocalPathPrefix + "api" + method.upper() + "Resource.yaml", "r")
        for line in f1.readlines():
            f2.write(line.replace("${RestApiId}", apiGateWayArgs["RestApiId"])
                     .replace("${PathPart}", apiGateWayArgs["PathPart"])
                     .replace("${ParentId}", apiGateWayArgs["ParentId"])
                     .replace("${lmdName}", apiGateWayArgs["LmdName"] + ":" + version)
                     .replace("${AuthorizerId}", apiGateWayArgs["AuthorizerId"])
                     )
        f1.close()
    f2.write("Transform: AWS::Serverless-2016-10-31")
    f2.close()


def lambda_handler(event, context):

    # 2 下载manage template文件
    download_s3_file(manageTemplateS3Key, manageTemplateS3Path, mangeLocalPath)
    # 读取manage.yaml文件内容
    manage_result = read_yaml_file(mangeLocalPath)
    manage_result["Resources"] = {}
    # print(manage_result)

    # 3 下载function的package.yaml文件 resourcePathPrefix + functionPath + "/package/package.yaml"
    functionName = event["trigger"]["functionName"]
    functionPath = event["trigger"]["prefix"] + "/" + functionName
    package_s3_key = "ph-platform"
    package_s3_path = resourcePathPrefix + functionPath + "/package/package.yaml"
    package_local_path = "/home/hbzhao/PycharmProjects/pythonProject/test/tmp/cicd/tmp/" + functionName + "/package.yaml"
    # 从s3下载yaml文件
    download_s3_file(package_s3_key, package_s3_path, package_local_path)

    # 4 将 function package文件内容写入 manage中
    package_result = read_yaml_file(package_local_path)
    manage_result["Resources"][functionName] = package_result["Resources"]["ATTFFunction"]
    if manage_result["Resources"][functionName].get("Metadata"):
        del manage_result["Resources"][functionName]["Metadata"]
    print(manage_result)

    # 5 将 api 相关信息写入到 manage中
    apiGateWayArgs = event["apiGateWayArgs"]
    write_yaml_file(manage_result, mangeLocalPath)
    write_api_resource(apiGateWayArgs, event["version"])
    # 6 上传manage文件 manageUrlPrefix + event["trigger"]["prefix"] + "/manage.yaml"
    upload_s3_file(
        bucket_name=manageTemplateS3Key,
        object_name=resourcePathPrefix + event["trigger"]["prefix"] + "/manage.yaml",
        file=mangeLocalPath
    )
    manageUrl = manageUrlPrefix + event["trigger"]["prefix"] + "/manage.yaml"
    print(manageUrl)
    # 创建resource cfn
    stackName = functionName + "-apiresource"
    stackParameters = {}
    print(stackName)
    return {
        "manageUrl": manageUrl,
        "stackName": stackName,
        "stackParameters": stackParameters
    }
