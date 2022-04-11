import json
from delegate.execute import Execute


def lambda_handler(event, context):
    # 11261502
    event = json.loads(event.get("Records")[0].get("body"))
    print(event)
    app = Execute(event=event, context=context)
    try:
        app.exec()
    except Exception as e:
        print("error: " + json.dumps(str(e), ensure_ascii=False))
    else:
        status = "success"
        print(status)
