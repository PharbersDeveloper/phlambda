import boto3
import os

def aws_cloudwatch_put_metric_data(project_id, project_name, current_user_id, current_name, action_mode, action_detail, value=None, unit=None):
    name_space = os.getenv("NAME_SPACE")
    metric_name = os.getenv("METRIC_NAME")
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
                    #'Timestamp': datetime(2022,3,31),
                    'Value': value if value else 1,
                    'Unit': unit if unit else 'Count',
                }
            ]
        )
    except Exception as e:
        resp = str(e)
    print(resp)
    return resp