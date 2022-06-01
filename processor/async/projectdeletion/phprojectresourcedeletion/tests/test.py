
import pytest
from src.main import lambda_handler


event = {
	"common": {
		"traceId": "Pharbers-Schedule-Stop-TraceId",
		"tenantId": "zudIcG_17yj8CEUoCTHg",
		"projectId": "1qxPsO7lzQAU6Yx",
		"projectName": "ABC",
		"owner": "alfred",
		"showName": "alfred"
	},
	"action": {
		"cat": "projectClear",
		"desc": "terminate project",
		"comments": "something need to say",
		"message": "something need to say",
		"required": True
	},
	"resources": {"traceId": "alfred-resource-creation-traceId", "engine": {"ClusterID": "j-PX68RDFOX82D", "ClusterDNS": "ec2-52-82-68-6.cn-northwest-1.compute.amazonaws.com.cn"}, "olap": {"PrivateIp": "192.168.55.39", "PublicIp": "69.230.248.188", "PrivateDns": "ip-192-168-55-39.cn-northwest-1.compute.internal", "PublicDns": "ec2-69-230-248-188.cn-northwest-1.compute.amazonaws.com.cn"}},
	"notification": {
		"required": True
	}
}


class TestLmd:

    def test_lmd(self):
        report = lambda_handler(event, None)
        print(report)


if __name__ == '__main__':
    TestLmd().test_lmd()
