import json
import boto3


'''
这个从resource表中读取需要创建的资源的matedata的描述
这里通过matadata的描述启动emr
调用以前的emr启动流程

args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "resources": [
        "emr", "ec2"
    ]，
    "metadata": {
        "engine": 
            {   
                "type": "ec2",
                "cfn": "",
                "parameters": {
                    "RootVolumeSize": 10,
                    "ReleaseLabel": "emr-6.2.0",
                    "MasterInstanceType": "m5.2xlarge",
                    "MasterStorage": 64,
                    "CoreInstanceType": "m5.2xlarge"
                    "CoreStorage": 32,
                    "InitialCoreSize": 1,
                    "MaxCoreSize": 2，
                    "TaskInstanceType": "m5.2xlarge",
                    "TaskStorage": 32,
                    "TaskNodeOutThreshold": 10,
                    "InitialTaskSize": 2,
                    "MaxTaskSize": 10
                }
            }
        ,
    }
}

return = {
    
}
'''


def create_cloudformation(stackName, cfn_path, parameters):
    cfn_client = boto3.client("cloudformation")
    res = cfn_client.create_stack(
        StackName=stackName,
        TemplateURL=cfn_path,
        Parameters=parameters
    )

    return res


def create_cloudformation_parameters(parameters):

    cfn_parameters = []
    parameter_tmp = {}
    for parameterKey, parameterValue in parameters.items():
        parameter_tmp["ParameterKey"] = parameterKey
        parameter_tmp["ParameterValue"] = parameterValue
        cfn_parameters.append(parameter_tmp)

    return cfn_parameters


def lambda_handler(event, context):

    # 获取参数 创建cloudformation
    if event["engine"]["type"] == "ec2":
        # 处理创建cloudformation参数
        cfn_parameters = create_cloudformation_parameters(event["engine"]["parameters"])
        cfn_res = create_cloudformation("emr-" + event["tenantId"], event["engine"]["cfn"], cfn_parameters)

    return True
