import os
import pytest
import json
import src.main as main
import src.app as app


class TestLmd:
    def test_lmd(self):
        event = open("../events/event.json", "r").read()
        # result = main.lambda_handler(json.loads(event), None)
        result = app.lambda_handler(json.loads(event), None)
        print(result)
        # assert 'e' in a


if __name__ == '__main__':
    os.environ["PATH_PREFIX"] = "/Users/qianpeng/Desktop/"
    os.environ["BATCH_SIZE"] = "200"
    os.environ["CLICKHOUSE_HOST"] = "127.0.0.1"
    os.environ["CLICKHOUSE_PORT"] = "19000"
    os.environ["CLICKHOUSE_DB"] = "default"
    os.environ["REDIS_HOST"] = "127.0.0.1"
    os.environ["REDIS_PORT"] = "6379"
    os.environ["LOCK_APP_NAME"] = "ds2clickhouse"
    os.environ["CHECK_APP_NAME"] = "rmds"
    os.environ["AWS_ACCESS_KEY_ID"] = "ASIAWPBDTVEAGO6BFMK2"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "9UJaxWAwwcHfB0vT6SeI9Sgrzo8u1IuUP05t9Gaa"
    os.environ["AWS_SESSION_TOKEN"] = "IQoJb3JpZ2luX2VjEGQaDmNuLW5vcnRod2VzdC0xIkcwRQIhAJ1p3kvQAkTnn7Z010iFlXV9eMhWiKbwh3UdjGmPijp9AiAOhbknNRReiU/dcnvP+II6fv+6wyYEiYbJKIU+ief01yqgAgiR//////////8BEAIaDDQ0NDYwMzgwMzkwNCIMnw6i+q8Hl5jj/WuQKvQBD9tji8MJR4XfFFsBiDFA7PA/mYINJqMYjeBN++w97prw1F/3DxOYaAF9PVd7bm5efo6ZN8vDzCXipHEeW03AzK1sB5Y+sTicY0V36zuhEa0Aa2sEfsV+wemYIayTCWxDmfyuX6448rIEO+oep27ni+Bok6vicsqv/o2AT7M7SSP+Ue8HNHa4tfnrA+q2HrQYp7QXYZZXyZ8qqhQNQnlKu3HzPVeXjVJAr7+EzFC/3ZWlFE28LcDHBFHVnZdFCrytew72Vmuu/f7roB+V8RQ0OQAWPuwalJeG/DmjaJne6TS6qLZbdX8LX4axAWyff58O3RpQKzDJse2MBjqdAWy8FOTlcYtq0UNVWRjUkurRhaxJMgw3re8di214+BHBUTLmFx3Vilv9YXWihAHv1YPZXaPCEYt6iVClfNWqoVsWDQlMIGEq1o8InoXfRC8VjHiCL1akd0IxHWsJPpCfccVOMtWg+Qfo9fXv6uR19s/yESN5zmMEGr+d8CrN/T5iLjbIapyemxCEVKaovyYN1EoMp+ql/ZM/dwNZvhM="
    pytest.main()
