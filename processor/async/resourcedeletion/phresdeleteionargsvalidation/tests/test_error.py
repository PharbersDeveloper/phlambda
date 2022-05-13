
import pytest
from src.main import lambda_handler


event = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "createDataset",
        "desc": "create intermediate dataset",
        "comments": "something need to say",
        "message": "something need to say",
        "required": True
    },
    "datasets": [
        {
            "name": "test_name",
            "cat": "intermediate",
            "format": "parquet"
        }
    ],
    "scripts":
        {
            "actionName": "compute_C2",
            "flowVersion": "developer",
            "inputs": "[]",
            "output": "{}"
        },
    "notification": {
        "required": True
    },
    "result": {
        "datasets": [""],
        "scripts": [""],
        "links": [""]
    }
}

event1 = {

    "action": {
        "cat": "createDataset",
        "desc": "create intermediate dataset",
        "comments": "something need to say",
        "message": "something need to say",
        "required": True
    },
    "datasets": [
        {
            "name": "test_name",
            "cat": "intermediate",
            "format": "parquet"
        }
    ],
    "scripts":
        {
            "actionName": "compute_C2",
            "flowVersion": "developer",
            "inputs": "[]",
            "output": "{}"
        },
    "notification": {
        "required": True
    },
    "result": {
        "datasets": [""],
        "scripts": [""],
        "links": [""]
    }
}

event2 = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },

    "datasets": [
        {
            "name": "test_name",
            "cat": "intermediate",
            "format": "parquet"
        }
    ],
    "scripts":
        {
            "actionName": "compute_C2",
            "flowVersion": "developer",
            "inputs": "[]",
            "output": "{}"
        },
    "notification": {
        "required": True
    },
    "result": {
        "datasets": [""],
        "scripts": [""],
        "links": [""]
    }
}
event3 = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "createDataset",
        "desc": "create intermediate dataset",
        "comments": "something need to say",
        "message": "something need to say",
        "required": True
    },
    "datasets": [
        {
            "name": "test_name",
            "cat": "intermediate",
            "format": "parquet"
        }
    ],
    "scripts": [
        {
            "actionName": "compute_C2",
            "flowVersion": "developer",
            "inputs": "[]",
            "output": "{}"
        }
    ],

    "result": {
        "datasets": [""],
        "scripts": [""],
        "links": [""]
    }
}
event4 = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "createDataset",
        "desc": "create intermediate dataset",
        "comments": "something need to say",
        "message": "something need to say",
        "required": True
    },

    "notification": {
        "required": True
    },
    "result": {
        "datasets": [""],
        "scripts": [""],
        "links": [""]
    }
}
event5 = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "createDataset",
        "desc": "create intermediate dataset",
        "comments": "something need to say",
        "message": "something need to say",
        "required": True
    },
    "datasets": [
        {
            "name": "test_name",
            "cat": "intermediate",
            "format": "parquet"
        }
    ],
    "scripts":[
        {
            "actionName": "compute_C2",
            "flowVersion": "developer",
            "inputs": "{}",
            "output": "{}"
        }],
    "notification": {
        "required": True
    },
    "result": {
        "datasets": [""],
        "scripts": [""],
        "links": [""]
    }
}

event6 = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "createDataset",
        "desc": "create intermediate dataset",
        "comments": "something need to say",
        "message": "something need to say",
        "required": True
    },
    "datasets": [
        {
            "name": "test_name",
            "cat": "intermediate",
            "format": "parquet"
        }
    ],
    "scripts":
        {
            "actionName": "compute_C2",
            "flowVersion": "developer",
            "inputs": "[]",
            "output": "[]"
        },
    "notification": {
        "required": True
    },
    "result": {
        "datasets": [""],
        "scripts": [""],
        "links": [""]
    }
}

event7 = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "YZYijD17N9L6LXx",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "createDataset",
        "desc": "create intermediate dataset",
        "comments": "something need to say",
        "message": "something need to say",
        "required": True
    },
    "datasets": [
        {
            "name": "cn_corp_ref",
            "cat": "intermediate",
            "format": "parquet"
        }
    ],
    "scripts":
        {
            "actionName": "compute_C2",
            "flowVersion": "developer",
            "inputs": "[]",
            "output": "{}"
        },
    "notification": {
        "required": True
    },
    "result": {
        "datasets": [""],
        "scripts": [""],
        "links": [""]
    }
}

event8 = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "zoY7FehqWl7NeEI",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "createDataset",
        "desc": "create intermediate dataset",
        "comments": "something need to say",
        "message": "something need to say",
        "required": True
    },
    "datasets": [
        {
            "name": "test_name",
            "cat": "intermediate",
            "format": "parquet"
        }
    ],
    "scripts":
        {
            "actionName": "compute_C2",
            "flowVersion": "developer",
            "inputs": "[]",
            "output": "{}"
        },
    "notification": {
        "required": True
    },
    "result": {
        "datasets": [""],
        "scripts": [""],
        "links": [""]
    }
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

    def test_common(self):
        report = lambda_handler(event1, None)
        print(report)

    def test_action(self):
        report = lambda_handler(event2, None)
        print(report)

    def test_notification(self):
        report = lambda_handler(event3, None)
        print(report)

    def test_datset_scripts(self):
        report = lambda_handler(event4, None)
        print(report)

    def test_lmd_scripts_type_allldict(self):
        report = lambda_handler(event5, None)
        print(report)

    def test_lmd_scripts_type_alllist(self):
        report = lambda_handler(event6, None)
        print(report)

    def test_lmd_datasets_name(self):
        report = lambda_handler(event7, None)
        print(report)

    def test_lmd_scripts_name(self):
        report = lambda_handler(event8, None)
        print(report)


if __name__ == '__main__':
    TestLmd().test_lmd()
