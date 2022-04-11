import json
from execute import Execute


def lambda_handler(event, context):
    # 11261502
    print(event)
    app = Execute(event=event, context=context)
    try:
        app.exec()
    except Exception as e:
        print("error: " + json.dumps(str(e), ensure_ascii=False))
    else:
        status = "success"
        print(status)
