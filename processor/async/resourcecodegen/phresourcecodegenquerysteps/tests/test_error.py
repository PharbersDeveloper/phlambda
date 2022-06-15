
import pytest
from src.main import lambda_handler

event = {
  "projectId": "ggjpDje0HUC2JW",
  "projectName":"demo",
  "flowVersion":"developer",
  "jobName": "compute_out2",
}


# 1. common 必须存在
# 2. action 必须存在
# 3. notification 必须存在
# 4. datasets 和 scripts 必须存在一个
#   4.1 如果dataset存在，name, cat, format 都必须存在，并判断类型
#   4.2 如果scripts存在，name, flowVersion, input, output 都必须存在，并判断类型


class TestLmd:
    def test_lmd(self):
        report = lambda_handler(event, None)
        print(report)


if __name__ == '__main__':
    TestLmd().test_lmd()
