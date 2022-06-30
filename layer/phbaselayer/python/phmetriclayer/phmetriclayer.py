import boto3
from datetime import datetime

'''
Namespace： <pharbers-platform>
metric: platform-usage
'''

def aws_cloudwatch_put_metric_data(NameSpace, MetricName, **kwargs):
    prefix_of_dict = ["Name", "Value"]
    kwargs_of_dimensions = list(kwargs.items())
    dimensions = list(map(lambda x: dict(zip(prefix_of_dict, list(x))), kwargs_of_dimensions))

    try:
        CWclient = boto3.client('cloudwatch')
        # put project-monitor metric
        resp = CWclient.put_metric_data(
            Namespace=NameSpace,
            MetricData=[
                {
                    'MetricName': MetricName,
                    'Dimensions': dimensions,
                    'Timestamp': datetime.now().strftime(format="%Y-%m-%d %H:%M:%S"),
                    'Value': 1,
                    'Unit': 'Count',
                }
            ]
        )
    except Exception as e:
        resp = str(e)
    print(resp)
    return resp