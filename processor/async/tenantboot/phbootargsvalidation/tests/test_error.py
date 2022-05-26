
import pytest
from src.main import lambda_handler


event = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "tenantId": "zudIcG_17yj8CEUoCTHg",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "tenantStart",
        "desc": "reboot project",
        "comments": "something need to say",
        "message": "something need to say",
        "required": True
    },
    "resources": [
        "emr", "clickhouse", "chproxy"
    ],
    "notification": {
        "required": True
    }
}


# 1. action.cat 只能是 tenantStart
# 2. resources 当前只能是以下值的一种
#     2.1 emr: 暂时不支持，只是为以后project reboot => tenant reboot 做准备
#     2.2 ec2 (deprecated 以后会被无服务器替换)
#     2.3 clickhouse: 暂时不支持，以后用ecs 构建解决
#     2.3 chproxy: 暂时不支持，以后用ecs 构建解决
#     2.4 dns (deprecated 以后会被无服务器替换)
#     2.5 target group (deprecated 以后会被无服务器替换)
#     2.7 load balance rule (deprecated 以后会被无服务器替换)
# 3. 当resource不存在的时候，启动全部记录在数据库中的参数


class TestLmd:
    def test_lmd(self):
        report = lambda_handler(event, None)
        print(report)


if __name__ == '__main__':
    TestLmd().test_lmd()
