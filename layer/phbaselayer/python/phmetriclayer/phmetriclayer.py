import boto3
from datetime import datetime

'''
Namespace： <pharbers-platform>
metric: <tenant-id>
'''

def aws_cloudwatch_put_metric_data(name_space, metric_name, project_id, project_name, current_user_id, current_name, action_mode, action_detail, value=None, unit=None):
    #name_space = os.getenv("NAME_SPACE")
    #metric_name = os.getenv("METRIC_NAME")
    prefix_of_dict = ["Name", "Value"]
    dimensions_parmateters = [("projectId", project_id),
                              ("projectName", project_name),
                              ("currentUser", current_user_id),
                              ("currentName", current_name),
                              ("action", action_mode),
                              ("actionDetail", action_detail)]

    dimensions = list(map(lambda x: dict(zip(prefix_of_dict, list(x))), dimensions_parmateters))
    try:
        CWclient = boto3.client('cloudwatch')
        # put project-monitor metric
        resp = CWclient.put_metric_data(
            Namespace=name_space,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': dimensions,
                    'TimeStamp': datetime.now().strftime(format="%Y-%m-%d %H:%M:%S"),
                    'Value': value if value else 1,
                    'Unit': unit if unit else 'Count',
                }
            ]
        )
    except Exception as e:
        resp = str(e)
    print(resp)
    return resp