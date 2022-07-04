import pytest
import src.main as app


class TestGenerateCode:
    def test_generate(self):
        event = {
            "traceId": "alex_test_traceId",
            "projectId": "ggjpDje0HUC2JW",
            "projectName": "demo",
            "flowVersion": "developer",
            "dagName": "demo",
            "owner": "hbzhao",
            "showName": "赵浩博",
            "script": {
                "jobName": "compute_BB",
                "runtime": "topn",
                "jobPath": "",
                "inputs": ["A", "B", "C"],      # 现在没用，可能以后有用
                "outputs": [],            # 现在没用，可能以后有用
                "id": "001"
            },
            "steps": [                  # 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
                {
                    "id": "alextest_demo_demo_developer_compute_十多个",
                    "stepId": "1",
                    "index": "1",
                    "runtime": "topn",
                    "stepName": "Initial Filter On Value",
                    "ctype": "FillEmptyWithValue",
                    "groupIndex": 0,
                    "groupName": "",
                    "expressionsValue": "JSON",
                    "expressions": {
                        "params": {
                            "preFilters": [
                                {
                                    "ds": "A",
                                    "preFilter": {
                                        "distinct": False,
                                        "enabled": True,
                                        "expr": "`商品名称` = '立普妥' AND `剂型` = 'TAB'"
                                    }
                                },
                                {
                                    "ds": "B",
                                    "preFilter": {
                                        "distinct": False,
                                        "enabled": True,
                                        "expr": "`剂型` = 'TAB'"
                                    }
                                }
                            ],
                            "preJoinComputedColumns": [
                                {
                                    "ds": "A",
                                    "computedColumns": [
                                        {
                                            "name": "拼接列",
                                            "type": "string",
                                            "expr": 'concat_ws("", `11111`, `商品名称`)'
                                        }
                                    ]
                                }
                            ],
                            "joins": [
                                {
                                    "datasets": [
                                        {
                                            "name": "A",
                                            "index": 0
                                        },
                                        {
                                            "name": "B",
                                            "index": 1
                                        }
                                    ],
                                    "caseInsensitive": False,
                                    "normalizeText": False,
                                    "type": "LEFT",
                                    "on": [
                                        {
                                            "type": "=",
                                            "conditions": [
                                                {
                                                    "ds": "A",
                                                    "column": "11111"
                                                },
                                                {
                                                    "ds": "B",
                                                    "column": "商品名称"
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "datasets": [
                                        {
                                            "name": "B",
                                            "index": 1
                                        },
                                        {
                                            "name": "C",
                                            "index": 2
                                        }
                                    ],
                                    "caseInsensitive": False,
                                    "normalizeText": False,
                                    "type": "LEFT",
                                    "on": [
                                        {
                                            "type": "=",
                                            "conditions": [
                                                {
                                                    "ds": "B",
                                                    "column": "商品名称"
                                                },
                                                {
                                                    "ds": "C",
                                                    "column": "商品名称"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "selectedColumns": [
                                {
                                    "ds": "A",
                                    "prefix": "prefix",
                                    "type": "select",
                                    "columns": ["11111", "商品名称", "生产企业", "剂型", "规格", "包装数量", "包装单位", "version"]
                                },
                                {
                                    "ds": "B",
                                    "prefix": "",
                                    "type": "autoselectall",
                                    "columns": []
                                },
                                {
                                    "ds": "C",
                                    "prefix": "123",
                                    "type": "select",
                                    "columns": ["商品名称"]
                                }
                            ],
                            "postJoinComputedColumns": [
                                {
                                    "name": "小风车",
                                    "type": "double",
                                    "expr": 'concat_ws("", `通用名称`, `商品名称`)'
                                }
                            ],
                            "postFilter": {
                                "distinct": True,
                                "enabled": True,
                                "expr": ""
                            }
                        }
                    }
                },
            ]
        }

        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()


