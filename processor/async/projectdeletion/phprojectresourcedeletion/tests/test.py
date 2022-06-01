
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
	"resources": {"host": "", "port": ""},
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
