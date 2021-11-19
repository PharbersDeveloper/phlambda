import handler.ClearClickHouseData as CD


class AppLambdaDelegate:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def exec(self):
        event = self.event
        records = event["Records"]
        for record in records:
            print('EventID: ' + record['eventID'])
            print('EventName: ' + record['eventName'])
            print(record)
            eventName = record["eventName"].lower()
            if eventName == "insert":
                new_image = record["dynamodb"]["NewImage"]
                jobCat = new_image["jobCat"]["S"]
                CD.run(eventName, jobCat, new_image)
            else:
                continue


