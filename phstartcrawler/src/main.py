
import boto3
import uuid
import time
import string, random

def lambda_handler(event, context):

    p_output = event["parameters"][0]['p_output']
    S3TargetPath = "/".join(p_output.split("/")[:-1])
    cfn_client = boto3.client("cloudformation")
    crawlerName = "crawler-" + ''.join(random.sample(string.ascii_letters, 10))
    print(type(crawlerName))
    print(crawlerName)
    cfn_client.create_stack(
        StackName= crawlerName,
        TemplateURL='https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cloudformation/glue/crawler/phcrawler.yaml',
        Parameters=[
            {
                'ParameterKey': 'DatabaseName',
                'ParameterValue': 'phetltemp',
            },
            {
                'ParameterKey': 'CrawlerName',
                'ParameterValue': crawlerName,
            },
            {
                'ParameterKey': 'S3TargetPath',
                'ParameterValue': S3TargetPath,
            }
        ]
    )
    glue_client = boto3.client('glue')


    create_status = 0
    get_crawlers_response = glue_client.get_crawlers()
    while get_crawlers_response:
        time.sleep(5)
        print(1)
        get_crawlers_response = glue_client.get_crawlers()
        for crawler in get_crawlers_response['Crawlers']:
            print(crawler['Name'])
            if crawler['Name'] == crawlerName:
                response = glue_client.start_crawler(
                    Name=crawlerName
                )
                create_status = 1
                break
        if create_status == 1:
            break


    while response:
        print(2)
        time.sleep(5)
        crawler_response = glue_client.get_crawler(
            Name=crawlerName
        )
        LastCrawl = crawler_response['Crawler'].get("LastCrawl", None)
        print(LastCrawl)
        if LastCrawl:
            cfn_client.delete_stack(
                StackName=crawlerName
            )
            break
