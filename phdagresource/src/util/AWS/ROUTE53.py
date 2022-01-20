import boto3
from util.AWS.PhAWS import PhAWS

class ROUTE53(PhAWS):

    def __init__(self, **kwargs):

        self.route53_client = boto3.client("route53")

    def create_records(self, records_name):

        self.route53_client.change_resource_record_sets(
            HostedZoneId='Z09499092IIZRWBTGZQWT',
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': records_name + '.pharbers.com',
                            'Type': 'A',
                            'SetIdentifier': 'Simple routing',
                            # 'Weight': 123,
                            'Region': 'cn-northwest-1',
                            # 'GeoLocation': {
                            #     'ContinentCode': 'string',
                            #     'CountryCode': 'string',
                            #     'SubdivisionCode': 'string'
                            # },
                            # 'Failover': 'PRIMARY'|'SECONDARY',
                            # 'MultiValueAnswer': True|False,
                            # 'TTL': 300,
                            # 'ResourceRecords': [
                            #     {
                            #         'Value': 'string'
                            #     },
                            # ],
                            'AliasTarget': {
                                'HostedZoneId': 'ZM7IZAIOVVDZF',
                                'DNSName': 'dualstack.alb-pharber-management-tools-2138063238.cn-northwest-1.elb.amazonaws.com.cn.',
                                'EvaluateTargetHealth': True
                            },
                            # 'HealthCheckId': 'string',
                            # 'TrafficPolicyInstanceId': 'string'
                        }
                    },
                ]
            }
        )

    def delete_records(self, records_name):

        self.route53_client.change_resource_record_sets(
            HostedZoneId='Z09499092IIZRWBTGZQWT',
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'DELETE',
                        'ResourceRecordSet': {
                            'Name': records_name + '.pharbers.com',
                            'Type': 'A',
                            'SetIdentifier': 'Simple routing',
                            # 'Weight': 123,
                            'Region': 'cn-northwest-1',
                            # 'GeoLocation': {
                            #     'ContinentCode': 'string',
                            #     'CountryCode': 'string',
                            #     'SubdivisionCode': 'string'
                            # },
                            # 'Failover': 'PRIMARY'|'SECONDARY',
                            # 'MultiValueAnswer': True|False,
                            # 'TTL': 300,
                            # 'ResourceRecords': [
                            #     {
                            #         'Value': 'string'
                            #     },
                            # ],
                            'AliasTarget': {
                                'HostedZoneId': 'ZM7IZAIOVVDZF',
                                'DNSName': 'dualstack.alb-pharber-management-tools-2138063238.cn-northwest-1.elb.amazonaws.com.cn.',
                                'EvaluateTargetHealth': True
                            },
                            # 'HealthCheckId': 'string',
                            # 'TrafficPolicyInstanceId': 'string'
                        }
                    },
                ]
            }
        )