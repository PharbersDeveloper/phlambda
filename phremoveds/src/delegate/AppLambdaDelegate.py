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

            new_image = record["dynamodb"]["NewImage"]
            eventName = record["eventName"].lower()
            jobCat = new_image["jobCat"]["S"]

            CD.run(eventName, jobCat, new_image)
        # try:
        #
        #
        # except Exception as e:
        #     print(e)
