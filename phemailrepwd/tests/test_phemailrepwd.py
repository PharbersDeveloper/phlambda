import json
import pytest
from phemailrepwd.src.main import lambdaHandler


class TestLmd:
    def test_lmd(self):
        data = {"type": "test", "address": "2091038466@qq.com", "subject": "密码修改", "attachment": None}
        assert "修改密码的网址发送成功" == json.loads(lambdaHandler(data, ' ')['body'])

    def test_lmd1(self):
        attachment = [
            {"file_name": "test1.yaml",
             "file_context": ['PH_NOTICE_EMAIL:\n', '  metadata:\n', '    name: PH_NOTICE_EMAIL\n']},
            {"file_name": "test2.txt", "file_context": ["xxxxxxxxxxxxxxxxxx"]},
            # {"file_name" : "test3.png", "file_context" : ["xxxxxxxxxxxxxxxxxx"]}
        ]
        data = {"type": "forget_password", "address": "2091038466@qq.com", "subject": "密码修改",
                "attachment": attachment}
        assert "文件发送成功" == json.loads(lambdaHandler(data, ' ')['body'])


if __name__ == '__main__':
    pytest.main()
