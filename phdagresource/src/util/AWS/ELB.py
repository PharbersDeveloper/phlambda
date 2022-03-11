import boto3
import random
from util.AWS.PhAWS import PhAWS

class ELB(PhAWS):

    def __init__(self, **kwargs):

        self.elb_client = boto3.client('elbv2')

    def create_target_group(self, project_id, target_port):

        response = self.elb_client.create_target_group(
            Name=project_id,
            Protocol='HTTP',
            ProtocolVersion='HTTP1',
            Port=target_port,
            VpcId='vpc-082167a9cbf8811e1',
            HealthCheckProtocol='HTTP',
            HealthCheckPort='traffic-port',
            HealthCheckEnabled=True,
            HealthCheckPath='/',
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=5,
            HealthyThresholdCount=5,
            UnhealthyThresholdCount=2,
            Matcher={
                'HttpCode': '302'
            },
            TargetType='ip',
        )

        return response.get("TargetGroups")[0].get("TargetGroupArn")

    def register_targets(self, target_group_arn, targets):

        self.elb_client.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=targets
        )

    def get_rules_len(self):

        response = self.elb_client.describe_rules(
            ListenerArn="arn:aws-cn:elasticloadbalancing:cn-northwest-1:444603803904:listener/app/alb-pharber-management-tools/66c1e8eef4d28433/27e4c643619d1c70",
        )
        Prioritys = [rule.get("Priority") for rule in response["Rules"]]

        Priority = str(random.randint(1, 99))
        while 1:
            if Priority not in Prioritys:
                break
            elif Priority in Prioritys:
                Priority = str(random.randint(1, 99))

        return Priority

    def create_rule(self, project_id, target_group_arn):

        Priority = self.get_rules_len()
        response = self.elb_client.create_rule(
            ListenerArn="arn:aws-cn:elasticloadbalancing:cn-northwest-1:444603803904:listener/app/alb-pharber-management-tools/66c1e8eef4d28433/27e4c643619d1c70",
            Priority=Priority,
            Conditions=[
                {
                    "Field": "host-header",
                    # "Values": ['auto-max-refactor.pharbers.com'],
                    "HostHeaderConfig": {
                        "Values": [project_id + ".pharbers.com"]
                    }
                }
            ],
            Actions=[
                {
                    "Type": "forward",
                    "TargetGroupArn": target_group_arn,
                    "Order": 1,
                    "ForwardConfig": {
                        "TargetGroups": [
                            {
                                "TargetGroupArn": target_group_arn,
                                "Weight": 1
                            },
                        ],
                        "TargetGroupStickinessConfig": {
                            "Enabled": True,
                            "DurationSeconds": 86400
                        }
                    }
                }
            ]
        )

        return response["Rules"][0]["RuleArn"]

    def delete_rule(self, rule_arn):

        response = self.elb_client.delete_rule(
            RuleArn=rule_arn
        )

    def delete_target_group(self, target_group_arn):

        response = self.elb_client.delete_target_group(
            TargetGroupArn=target_group_arn
        )
