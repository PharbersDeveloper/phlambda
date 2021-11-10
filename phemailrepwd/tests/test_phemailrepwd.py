import json
import pytest
from phemailrepwd.src.main import lambdaHandler


class TestLmd:
    def test_lmd(self):
        data = {
            "body": "{\"content_type\": \"test\", \"target_address\": [\"2091038466@qq.com\"],\n  \"subject\": \"密码修改\",\n  \"attachments\": [{\"file_name\": \"test1.yaml\",\n    \"file_context\": [\"PH_NOTICE_EMAIL:\", \"metadata:\", \"name: PH_NOTICE_EMAIL\"]},\n    {\"file_name\": \"test2.txt\", \"file_context\": [\"xxxxxxxxxxxxxxxxxx\"]}]}"}
        assert "file_sucess" == json.loads(lambdaHandler(data, ' ')['body'])["message"]

    def test_lmd1(self):
        data = {
            "body": "{\"content_type\": \"forget_password\", \"target_address\": [\"2091038466@qq.com\"],\n  \"subject\": \"密码修改\",\n  \"attachments\": [{\"file_name\": \"test1.yaml\",\n    \"file_context\": [\"PH_NOTICE_EMAIL:\", \"metadata:\", \"name: PH_NOTICE_EMAIL\"]},\n    {\"file_name\": \"test2.txt\", \"file_context\": [\"xxxxxxxxxxxxxxxxxx\"]}]}"}
        assert "password_change_sucess" == json.loads(lambdaHandler(data, ' ')['body'])["message"]


if __name__ == '__main__':
    pytest.main()
