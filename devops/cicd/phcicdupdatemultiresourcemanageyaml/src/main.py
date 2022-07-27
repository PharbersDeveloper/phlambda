import yaml
import os
import time
import boto3
import math
import random

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

cfn_client = boto3.client('cloudformation')
manageTemplateS3Key = "ph-platform"
manageTemplateS3Path = "2020-11-11/cicd/template/manageApiTemplate.yaml"
apiTemplateS3Key = "ph-platform"
apiTemplateS3PathPrefix = "2020-11-11/cicd/template/"
TemplateS3Key = "ph-platform"
lmdVersionTemplateS3Path = "2020-11-11/cicd/template/lmdVersion.yaml"
lmdAliasTemplateS3Path = "2020-11-11/cicd/template/lmdAlias.yaml"
resourcePathPrefix = "2020-11-11/cicd/"
manageUrlPrefix = "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/"
mangeLocalPathPrefix = "/tmp/cicd/tmp/"
mangeLocalPathSuffix = "/manage.yaml"
dealMangeLocalPathPrefix = "/tmp/cicd/tmp/"
dealMangeLocalPathSuffix = "/deal_manage.yaml"
apiResourceLocalPathPrefix = "/tmp/cicd/tmp/"
lmdVersionLocalPath = "/tmp/cicd/tmp/lmdVersion.yaml"
lmdAliasLocalPath = "/tmp/cicd/tmp/lmdAlias.yaml"


class Ref(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return u"!Ref " + self.value

    def deal(self):
        return u"!Ref " + self.value


class GetAtt(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return u"!GetAtt " + self.value

    def deal(self):
        return u"!GetAtt " + self.value


def ref_constructor(loader, node):
    value = loader.construct_scalar(node)
    value = Ref(value)
    return str(value)


def getatt_constructor(loader, node):
    value = loader.construct_scalar(node)
    value = GetAtt(value)
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
    yaml.add_constructor(u'!GetAtt', getatt_constructor)  # 添加代码来构造一个Sub对象
    with open(file_path, encoding='utf-8') as file:
        result = yaml.load(file.read(), Loader=yaml.FullLoader)
    return result


def write_yaml_file(result, file_path):
    f = open(file_path, "w")
    # print(yaml.dump(result))
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


def write_api_resource(apiGateWayArgs, version, runtime, mangeLocalPath, resource_id_map,
                       resourceName, resourceValue):
    methods = resourceValue["methods"]
    auth = resourceValue["auth"]
    methods.insert(0, "Init")
    pathPart = resourceName.split("/")[-1]
    resourceId = resource_id_map[resourceName]["resourceId"]
    parentId = apiGateWayArgs["ParentId"]
    parentName = "/".join(resourceName.split("/")[:-1])
    if parentName and parentName not in apiGateWayArgs["ApiResourceId"].keys():
        parentId = "!Ref " + runtime.upper() + resource_id_map[parentName]["resourceId"] + "INITMETHOD"
    elif parentName and parentName in apiGateWayArgs["ApiResourceId"].keys():
        parentId = apiGateWayArgs["ApiResourceId"][parentName]


    f2 = open(mangeLocalPath, "a+")
    for method in methods:
        download_s3_file(
            apiTemplateS3Key,
            apiTemplateS3PathPrefix + auth.lower() + "Api/" + "api" + method.upper() + "Resource.yaml",
            apiResourceLocalPathPrefix + apiGateWayArgs["LmdName"] + "/api" + method.upper() + "Resource.yaml")
        f1 = open(apiResourceLocalPathPrefix + apiGateWayArgs["LmdName"] + "/api" + method.upper() + "Resource.yaml", "r")
        f2.write("  " + runtime.upper() + resourceId + method.upper() + "METHOD:\n")
        for line in f1.readlines():
            f2.write(line.replace("${RestApiId}", apiGateWayArgs["RestApiId"])
                     .replace("${PathPart}", "\"" + pathPart + "\"")
                     .replace("${ParentId}", parentId)
                     .replace("${ReplaceLmdName}", apiGateWayArgs["LmdName"] + ":" + version)
                     .replace("${AuthorizerId}", apiGateWayArgs["AuthorizerId"])
                     .replace("${ReplaceResource}", runtime.upper() + resourceId + "INITMETHOD")
                     )
        f1.close()
    f2.close()


def copy_manage_resource(bucket_name, prefix):
    copy_source = {
        'Bucket': bucket_name,
        'Key': prefix + "/manage.yaml"
    }
    s3_resource.meta.client.copy(copy_source, bucket_name, prefix + "/manage_back.yaml")


def generate():
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
              "abcdefghijklmnopqrstuvwxyz" \
              "0123456789"

    charsetLength = len(charset)
    keyLength = 3 * 5

    array = []
    for i in range(keyLength):
        array.append(charset[math.floor(random.random() * charsetLength)])

    return "".join(array)


def lambda_handler(event, context):
    print(event)
    apiGateWayArgs = event["apiGateWayArgs"]
    runtime = event["runtime"]
    mangeLocalPath = mangeLocalPathPrefix + event["multistage"]["functionName"] + mangeLocalPathSuffix
    dealMangeLocalPath = dealMangeLocalPathPrefix + event["multistage"]["functionName"] + dealMangeLocalPathSuffix
    # 2 下载manage template文件
    download_s3_file(manageTemplateS3Key, manageTemplateS3Path, mangeLocalPath)
    # 判断manage.yaml文件是否存在 存在则下载 对此文件进行更改
    if s3_file_exist("ph-platform", resourcePathPrefix + event["multistage"]["prefix"] + "/" +
                                    event["multistage"]["functionName"] + "/manage.yaml"):
        download_s3_file("ph-platform", resourcePathPrefix + event["multistage"]["prefix"] + "/" +
                         event["multistage"]["functionName"] + "/manage.yaml",
                         mangeLocalPath)
        copy_manage_resource("ph-platform", resourcePathPrefix + event["multistage"]["prefix"] + "/" + event["multistage"]["functionName"])
    else:
        # 如果不存在 从s3下载manage template文件
        download_s3_file(manageTemplateS3Key, manageTemplateS3Path, mangeLocalPath)
    manage_result = read_yaml_file(mangeLocalPath)
    if not manage_result.get("Resources"):
        manage_result["Resources"] = {}
    if manage_result.get("Transform"):
        del manage_result["Transform"]
    # 判断Resource 下以Runtime开头的 如果相同直接删除
    manage_result_resources = list(manage_result["Resources"].keys())
    for resourceName in manage_result_resources:
        if resourceName.startswith(runtime.upper()):
            del manage_result["Resources"][resourceName]
    # print(manage_result)

    # 3 下载function的package.yaml文件 resourcePathPrefix + functionPath + "/package/package.yaml"
    functionName = event["multistage"]["functionName"]
    functionPath = event["multistage"]["prefix"] + "/" + functionName
    package_s3_key = "ph-platform"
    package_s3_path = resourcePathPrefix + functionPath + "/package/package.yaml"
    package_local_path = "/tmp/" + functionName + "/package.yaml"
    # 从s3下载yaml文件
    download_s3_file(package_s3_key, package_s3_path, package_local_path)

    # 4 将 function package文件内容写入 manage中
    package_result = read_yaml_file(package_local_path)
    manage_result["Resources"][functionName] = package_result["Resources"]["ATTFFunction"]
    if manage_result["Resources"][functionName].get("Metadata"):
        del manage_result["Resources"][functionName]["Metadata"]
    ResourcePrefix = functionName + event["version"].replace("-", "")
    aliasResourcePrefix = functionName + "Alias" + event["version"].replace("-", "")
    versionResourcePrefix = functionName + "Version" + event["version"].replace("-", "")
    del_keys = []
    for key in manage_result["Resources"].keys():
        if key.startswith(ResourcePrefix) or key.startswith(event["version"]) or key.startswith(aliasResourcePrefix) \
                or key.startswith(versionResourcePrefix):
            del_keys.append(key)
    print(del_keys)
    if del_keys:
        for del_key in del_keys:
            del manage_result["Resources"][del_key]
    write_yaml_file(manage_result, mangeLocalPath)

    # 创建Version
    download_s3_file(TemplateS3Key, lmdAliasTemplateS3Path, lmdAliasLocalPath)
    download_s3_file(TemplateS3Key, lmdVersionTemplateS3Path, lmdVersionLocalPath)
    manage = open(mangeLocalPath, "a+")
    f1 = open(lmdVersionLocalPath, "r")
    f2 = open(lmdAliasLocalPath, "r")
    versionResourceName = apiGateWayArgs["LmdName"] + "Version" + event["version"].replace("-", "") + str(int(round(time.time() * 1000)))
    versionAlisaName = apiGateWayArgs["LmdName"] + "Alias" + event["version"].replace("-", "")
    manage.write("  " + versionResourceName + ":\n")
    for line in f1.readlines():
        manage.write(line.replace("${ReplaceLmdName}", apiGateWayArgs["LmdName"]))
    manage.write("\n")
    manage.write("  " + versionAlisaName + ":\n")
    for line in f2.readlines():
        manage.write(line.replace("${ReplaceLmdName}", apiGateWayArgs["LmdName"])
                     .replace("${ReplaceVersionResource}", versionResourceName)
                     .replace("${ReplaceVersion}", event["version"])
                     )
    manage.write("\n")
    manage.close()
    f2.close()
    f1.close()

    # 5 将 api 相关信息写入到 manage中

    pathParts = []
    resources = apiGateWayArgs["resources"]
    resource_id_map = {}
    for resource in resources:
        pathParts.append(resource["name"].split("/")[-1])
        resource_id_map[resource["name"]] = {}
        resource_id_map[resource["name"]]["methods"] = resource["methods"]
        resource_id_map[resource["name"]]["auth"] = resource["auth"]
        resource_id_map[resource["name"]]["resourceId"] = resource["name"]\
            .replace("/", "")\
            .replace("{", "0")\
            .replace("}", "0").upper()

    print(resource_id_map)
    for resourceName, resourceValue in resource_id_map.items():
        write_api_resource(apiGateWayArgs, event["version"], runtime, mangeLocalPath, resource_id_map,
                           resourceName, resourceValue)

    # 6 处理manage文件
    os.system("touch " + dealMangeLocalPath)
    m = open(mangeLocalPath, "a+")
    m.write("Transform: AWS::Serverless-2016-10-31")
    m.close()
    ff = open(mangeLocalPath, "r+")
    ff2 = open(dealMangeLocalPath, "r+")
    for line in ff.readlines():
        if "method.response.header.Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token" in line:
            line = "            \"method.response.header.Access-Control-Allow-Headers\": \"\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'\"\n"
        if "method.response.header.Access-Control-Allow-Methods: GET,OPTIONS,POST" in line:
            line = "            \"method.response.header.Access-Control-Allow-Methods\": \"\'GET,OPTIONS,POST\'\"\n"
        if "method.response.header.Access-Control-Allow-Origin: *" in line:
            line = "            \"method.response.header.Access-Control-Allow-Origin\": \"\'*\'\"\n"
        for pathPart in pathParts:
            if "      PathPart: " + pathPart in line:
                line = "      PathPart: " + "\"" + pathPart + "\"\n"

        ff2.write(line)
    ff.close()
    ff2.close()

    # 6 上传manage文件 manageUrlPrefix + event["multistage"]["prefix"] + "/manage.yaml"
    upload_s3_file(
        bucket_name=manageTemplateS3Key,
        object_name=resourcePathPrefix + event["multistage"]["prefix"] + "/" +
                    event["multistage"]["functionName"] + "/manage.yaml",
        file=dealMangeLocalPath
    )
    manageUrl = manageUrlPrefix + event["multistage"]["prefix"] + "/" + event["multistage"]["functionName"] + "/manage.yaml"
    print(manageUrl)
    # 创建resource cfn
    stackName = functionName + "-apiresource"
    stackParameters = {}

    return {
        "manageUrl": manageUrl,
        "stackName": stackName,
        "stackParameters": stackParameters
    }
