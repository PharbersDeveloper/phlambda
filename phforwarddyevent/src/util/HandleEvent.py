import json
#from phmetrixlayer import aws_cloudwatch_put_metric_data
from util.phmetrixlayer import aws_cloudwatch_put_metric_data

class HandleEvent(object):
    def __init__(self, event):
        self.Records = event['Records'][0]
        self.eventName = self.Records['eventName']
        self.dynamodb = self.Records['dynamodb']
        self.NewImage = self.dynamodb['NewImage']

    def get_jobCat(self):
        return self.NewImage['jobCat']['S']

    def get_jobDesc(self):
        return self.NewImage['jobDesc']['S']

    def get_owner(self):
        return self.NewImage['owner']['S']

    def get_id(self):
        return self.NewImage['id']['S']

    def get_comments(self):
        return self.NewImage['comments']['S']

    def get_projectId(self):
        return self.NewImage['projectId']['S']

    def get_message(self):
        return json.loads(self.NewImage['message']['S'])

    def get_date(self):
        return self.NewImage['date']['S']

class EventTracking(HandleEvent):

    def __init__(self, event):
        super().__init__(event)
        print("*"*50 + " Event tracking" + "*"*50)
        self.message = self.get_message()
        self.jobcat_with_contain_list = ["remove_DS", "remove_Job", "clear_DS_data"]

    def get_message(self):
        return super().get_message()

    def event_tracking_with_jobcat(self):

        project_id = super().get_projectId()
        if str(super().get_jobCat()).lower() in [str(x).lower() for x in self.jobcat_with_contain_list]:
            project_name = self.message[0]['projectName']
            current_user_id = self.message[0]['opname']
        else:
            project_name = self.message['projectName']
            current_user_id = self.message['opname']
        current_name = super().get_owner()
        action_mode = super().get_jobCat()
        action_detail = super().get_jobDesc()

        return aws_cloudwatch_put_metric_data(project_id,
                                              project_name,
                                              current_user_id,
                                              current_name,
                                              action_mode,
                                              action_detail)
