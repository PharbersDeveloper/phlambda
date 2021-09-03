import json
import os

from parse_event import Parse
from git_python import GitRepository
from package_code import zip_code

def lambda_handler(event, context):
    parse = Parse()
    print(event)

    git_event = parse.print_branch_information(event=event)
    print(git_event)
    if git_event['event_type'] == "UPDATE" and git_event['operator_name'] == "hbzhao":
        git_url = 'https://hbzhao:123456@bitbucket.pharbers.com/scm/lgc/phlambda.git'
        local_path_prefix = '/tmp'
        local_path = os.path.join(local_path_prefix, 'phlambda')
        repo = GitRepository(local_path, git_url, branch='feature/PBDP-1782-codebuild-testreport')

    zip_code()

    return {
        "statusCode": 200,
        "body": json.dumps("Hello from Lambda")
    }
