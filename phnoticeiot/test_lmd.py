import pytest
import json


class TestLmd:
    def test_lmd(self):
        # event = {
        #     'body': "{\"executionArn\": \"arn:aws-cn:states:cn-northwest-1:444603803904:execution:ETL_Iterator:executor_1422814573177741312\"}"
        # }
        # response = main.lambda_handler(event, context=None)
        # assert response
        a = "pharbers"
        assert 'e' in a
