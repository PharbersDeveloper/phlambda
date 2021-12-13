import json
from handler.Strategy.Reader import Reader
from handler.Command.MsgReceiver import MsgReceiver
from handler.Command.SendMsgCommand import SendMsgSuccessCommand, SendMsgFailCommand
from constants.Errors import Errors


def lambda_handler(event, context):
    records = event["Records"]
    history = {}
    try:
        data = []
        for record in records:
            if record["eventName"].lower() != "insert":
                continue

            new_image = record["dynamodb"]["NewImage"]
            if record["eventName"].lower() == "insert" and \
                    new_image.get("jobCat", {"S": "None"})["S"] == "project_file_to_DS":
                item = {}
                for field in list(new_image.keys()):
                    value = new_image[field]
                    v_k = list(value.keys())[0]
                    item[field] = value[v_k]
                data.append(item)

                for item in data:
                    item["message"] = json.loads(item["message"])
                    history = item
                    result = Reader(item).reader()

                    SendMsgSuccessCommand(MsgReceiver()).execute(result)

    except Errors as e:
        command = SendMsgFailCommand(MsgReceiver())
        command.execute({
            "id": history["id"],
            "project_id": history["projectId"],
            "prefix": "project_file_to_DS_",
            "owner": history["owner"],
            "showName": history["showName"],
            "opgroup": history["message"]["opgroup"],
            "error": {
                "code": e.code,
                "message": e.message
            }
        })
