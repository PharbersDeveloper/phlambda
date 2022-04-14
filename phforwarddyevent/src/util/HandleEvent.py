import json
from phmetrixlayer import aws_cloudwatch_put_metric_data
#from util.phmetrixlayer import aws_cloudwatch_put_metric_data

# TODO: HandlerEvent与EventTracking这层抽象继承其实是没有必要的原因有以下几点
# 1、你的HandlerEvent只是对数据进行解析而已，最简单的形式是将整个event你需要的数据进行Map化也就是形式Python的字典，根据字典这种数据结构进行操作
# 2、从考虑层面上看JobCat如果有增加并且格式又不一样的情况下，你的EventTracking必然要进行较大幅度的改动，这不符合里氏替换原则与模块化解耦
# 3、尽量不要使用Python的推导式，在数据量大的情况下有很大的问题
# 4、有logger模块要使用logger模块，不要用print来替代logger的作用
# 5、将项目中与你的逻辑无关的代码请删除，以免造成不必要的误会
# 6、单元测试是有pytest这个库来操作、对应的功能点要有对应的test测试用例，结果用assert进行断言判断
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
