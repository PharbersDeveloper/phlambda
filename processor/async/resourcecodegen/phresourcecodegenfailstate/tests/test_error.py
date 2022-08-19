
import pytest
from src.main import lambda_handler

event = {
  "common": {
    "traceId": "6e38938e0dbd4dc2bf1c50d6fc275bf1",
    "projectId": "ggjpDje0HUC2JW",
    "projectName": "demo",
    "flowVersion": "developer",
    "dagName": "demo",
    "owner": "c89b8123-a120-498f-963c-5be102ee9082",
    "showName": "张璐"
  },
  "action": {
    "cat": "createSteps",
    "desc": "create prepare steps",
    "comments": "something need to say",
    "message": "something need to say",
    "required": True
  },
  "script": {
    "id": "",
    "jobName": "compute_out2",
    "jobPath": "",
    "inputs": [],
    "outputs": [],
    "runtime": "prepare"
  },
  "steps": [
    {
      "pjName": "ggjpDje0HUC2JW_demo_demo_developer_compute_out2",
      "stepId": "1",
      "index": "1",
      "ctype": "FilterOnValue",
      "expressions": {
        "type": "FilterOnValue",
        "code": "pyspark",
        "params": {
          "values": [
            "阿乐"
          ],
          "matchingMode": "FULL_STRING",
          "normalizationMode": "EXACT",
          "action": "KEEP_ROW",
          "booleanMode": "AND",
          "appliesTo": "COLUMNS",
          "columns": [
            "商品名称"
          ]
        }
      },
      "runtime": "prepare",
      "groupName": "",
      "groupIndex": 0,
      "expressionsValue": "JSON",
      "stepName": "Initial Filter On Value",
      "id": "ggjpDje0HUC2JW_demo_demo_developer_compute_out21"
    },
    {
      "pjName": "ggjpDje0HUC2JW_demo_demo_developer_compute_out2",
      "stepId": "2",
      "index": "2",
      "ctype": "ReplaceValue",
      "expressions": {
        "type": "ValueReplace",
        "code": "pyspark",
        "params": {
          "mapping": [
            {
              "from": "TAB",
              "to": "TBA"
            }
          ],
          "columns": [
            "剂型"
          ],
          "matchingMode": "FULL_STRING"
        }
      },
      "runtime": "prepare",
      "groupName": "",
      "groupIndex": 0,
      "expressionsValue": "JSON",
      "stepName": "Initial Replace Value",
      "id": "ggjpDje0HUC2JW_demo_demo_developer_compute_out22"
    }
  ],
  "notification": {
    "required": True
  },
  "oldImage": [
    {
      "index": 1,
      "ctype": "FilterOnValue",
      "expressions": "{\"type\": \"FilterOnValue\", \"code\": \"pyspark\", \"params\": {\"values\": [\" 阿乐\"], \"matchingMode\": \"FULL_STRING\", \"normalizationMode\": \"EXACT\", \"action\": \"KEEP_ROW\", \"booleanMode\": \"AND\", \"appliesTo\": \"COLUMNS\", \"columns\": [\"商品名称\"]}}",
      "runtime": "prepare",
      "groupName": "",
      "groupIndex": 0,
      "pjName": "ggjpDje0HUC2JW_demo_demo_developer_compute_out2",
      "id": "ggjpDje0HUC2JW_demo_demo_developer_compute_out21",
      "expressionsValue": "JSON",
      "stepId": "1",
      "stepName": "Initial Filter On Value"
    },
    {
      "index": 2,
      "ctype": "ReplaceValue",
      "expressions": "{\"type\": \"ValueReplace\", \"code\": \"pyspark\", \"params\": {\"mapping\": [{\"from\": \"TAB\", \"to\": \"TBA\"}], \"columns\": [\"剂型\"], \"matchingMode\": \"FULL_STRING\"}}",
      "runtime": "prepare",
      "groupName": "",
      "groupIndex": 0,
      "pjName": "ggjpDje0HUC2JW_demo_demo_developer_compute_out2",
      "id": "ggjpDje0HUC2JW_demo_demo_developer_compute_out22",
      "expressionsValue": "JSON",
      "stepId": "2",
      "stepName": "Initial Replace Value"
    }
  ]
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
