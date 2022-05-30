import json
import boto3
from boto3.dynamodb.conditions import Key


'''
删除索引
包括表：
1. Scenario
2. Datasets
3. dagconf
4. dag
5. resource （*现在还没有*）
6. action
7. notification
8. dashboard
9. exectuion
10. executionStatus
11. logs
12. scenario_trigger
13. scenario_step
14. step
15. slide
16 version

args = {
    "traceId": "alfred-resource-creation-traceId",
    "projectId": "ggjpDje0HUC2JW",
    "projectName": "demo",
    "owner": "alfred",
    "showName": "alfred"
}
'''


def lambda_handler(event, context):
    return True


