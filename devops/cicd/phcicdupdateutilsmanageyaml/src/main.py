import yaml
import os
import time
import boto3
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
cfn_client = boto3.client('cloudformation')
manageTemplateS3Key = "ph-platform"
manageTemplateS3Path = "2020-11-11/cicd/template/manageUtilsTemplate.yaml"
apiTemplateS3Key = "ph-platform"
apiTemplateS3PathPrefix = "2020-11-11/cicd/template/"
TemplateS3Key = "ph-platform"
lmdVersionTemplateS3Path = "2020-11-11/cicd/template/lmdVersion.yaml"
lmdAliasTemplateS3Path = "2020-11-11/cicd/template/lmdAlias.yaml"
resourcePathPrefix = "2020-11-11/cicd/"
manageUrlPrefix = "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/"
mangeLocalPath = "/tmp/manage.yaml"
apiResourceLocalPathPrefix = "/tmp/"
lmdVersionLocalPath = "/tmp/lmdVersion.yaml"
lmdAliasLocalPath = "/tmp/lmdAlias.yaml"


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


def copy_manage_resource(bucket_name, prefix):
    copy_source = {
        'Bucket': bucket_name,
        'Key': prefix + "/manage.yaml"
    }
    s3_resource.meta.client.copy(copy_source, bucket_name, prefix + "/manage_back.yaml")


def lambda_handler(event, context):
    print(event)
    # 2 下载manage template文件
    download_s3_file(manageTemplateS3Key, manageTemplateS3Path, mangeLocalPath)
    # 判断manage.yaml文件是否存在 存在则下载 对此文件进行更改
    if s3_file_exist("ph-platform", resourcePathPrefix + event["utils"]["prefix"] + "/" +
                                    event["utils"]["functionName"] + "/manage.yaml"):
        download_s3_file("ph-platform", resourcePathPrefix + event["utils"]["prefix"] + "/" +
                         event["utils"]["functionName"] + "/manage.yaml",
                         mangeLocalPath)
        copy_manage_resource("ph-platform", resourcePathPrefix + event["utils"]["prefix"] + "/" + event["utils"]["functionName"])
    else:
        # 如果不存在 从s3下载manage template文件
        download_s3_file(manageTemplateS3Key, manageTemplateS3Path, mangeLocalPath)
    manage_result = read_yaml_file(mangeLocalPath)
    if not manage_result.get("Resources"):
        manage_result["Resources"] = {}
    if manage_result.get("Transform"):
        del manage_result["Transform"]
    # print(manage_result)

    # 3 下载function的package.yaml文件 resourcePathPrefix + functionPath + "/package/package.yaml"
    functionName = event["utils"]["functionName"]
    functionPath = event["utils"]["prefix"] + "/" + functionName
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
    versionResourceName = functionName + "Version" + event["version"].replace("-", "") + str(int(round(time.time() * 1000)))
    versionAlisaName = functionName + "Alias" + event["version"].replace("-", "")
    manage.write("  " + versionResourceName + ":\n")
    for line in f1.readlines():
        manage.write(line.replace("${ReplaceLmdName}", functionName))
    manage.write("\n")
    manage.write("  " + versionAlisaName + ":\n")
    for line in f2.readlines():
        manage.write(line.replace("${ReplaceLmdName}", functionName)
                     .replace("${ReplaceVersionResource}", versionResourceName)
                     .replace("${ReplaceVersion}", event["version"])
                     )
    manage.write("\n")
    manage.write("Transform: AWS::Serverless-2016-10-31")
    manage.close()
    f2.close()
    f1.close()

    # 6 上传manage文件 manageUrlPrefix + event["utils"]["prefix"] + "/manage.yaml"
    upload_s3_file(
        bucket_name=manageTemplateS3Key,
        object_name=resourcePathPrefix + event["utils"]["prefix"] + "/" +
                    event["utils"]["functionName"] + "/manage.yaml",
        file=mangeLocalPath
    )
    manageUrl = manageUrlPrefix + event["utils"]["prefix"] + "/" + event["utils"]["functionName"] + "/manage.yaml"
    print(manageUrl)
    # 创建resource cfn
    stackName = functionName + "-utilsresource"
    stackParameters = {}

    return {
        "manageUrl": manageUrl,
        "stackName": stackName,
        "stackParameters": stackParameters
    }