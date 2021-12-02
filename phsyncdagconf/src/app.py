import json
from delegate.max import Project
from delegate.execute import Execute




def lambda_handler(event, context):
    # 11261502
    print(event)
    app = Project(event=event, context=context)
    try:
        app.exec()
    except Exception as e:
        print("error: " + json.dumps(str(e), ensure_ascii=False))
    else:
        status = "success"
        print(status)
