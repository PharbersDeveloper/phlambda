import json
import handler.ClearClickHouseData as CD


class AppLambdaDelegate:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def exec(self):
        event = self.event
        event = json.loads(event.get("Records")[0].get("body"))
        records = event["Records"]
        for record in records:
            eventName = record["eventName"].lower()
            if eventName == "insert":
                new_image = record["dynamodb"]["NewImage"]
                jobCat = new_image.get("jobCat", {"S": "None"})["S"]
                CD.run(eventName, jobCat, new_image)
            else:
                continue


