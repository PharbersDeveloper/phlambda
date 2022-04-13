import json
from execute import Execute


def lambda_handler(event, context):
    print(event)
    app = Execute(event=event, context=context)
    try:
        app.exec()
    except Exception as e:
        print("error: " + json.dumps(str(e), ensure_ascii=False))
        status = "fail"
    else:
        status = "success"
    return status

