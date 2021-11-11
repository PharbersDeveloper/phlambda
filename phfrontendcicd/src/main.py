import json
import os

from parse_event import Parse
from git_python import GitRepository
from upload_code import zip_code, start_codebuild

def lambda_handler(event, context):
    # 测试cicd1548
    parse = Parse()
    print(event)

    git_event = parse.print_branch_information(event=event)
    print(git_event)
    if git_event.get("event_type") == "MERGED" and git_event.get("merge_branch_to") == "master":
        # os.environ['GIT_URL'] = "https://hbzhao:123456@bitbucket.pharbers.com/scm/fron/micro-frontend.git"
        git_url = os.getenv("GIT_URL")
        local_path = os.path.join("/tmp", git_event.get("merge_repository_to"))
        # 从bitbucket下载代码 存放在local_path下
        repo = GitRepository(local_path, git_url, branch=git_event.get("merge_branch_to"))
        print("clone success")
        # 打包上传代码到s3
        zip_code(local_path, git_event)

        # 启动codebuild
        start_codebuild()

        return {
            "statusCode": 200,
            "body": json.dumps("CICD Complete")
        }

    return {
        "statusCode": 200,
        "body": json.dumps("The git operation type is illegal")
    }

if __name__ == '__main__':
    event = {"eventKey":"pr:merged","date":"2021-11-02T15:34:46+0800","actor":{"name":"hbzhao","emailAddress":"hbzhao@data-pharbers.com","id":302,"displayName":"赵浩博","active":"true","slug":"hbzhao","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/users/hbzhao"}]}},"pullRequest":{"id":90,"version":2,"title":"Developer","description":"* 增加action接口\r\n* 修改readme文件\r\n* 上传回调修改\r\n* 官网报错修改\r\n* 上传页面修改\r\n* 重构一下，分离抽象\r\n* 重构抽象完成","state":"MERGED","open":"false","closed":"true","createdDate":1635838457000,"updatedDate":1635838485000,"closedDate":1635838485000,"fromRef":{"id":"refs/heads/developer","displayId":"developer","latestCommit":"a804dac354d042b4ca299c345473e720034ac0e6","repository":{"slug":"micro-frontend","id":69,"name":"micro-frontend","description":"微前端","scmId":"git","state":"AVAILABLE","statusMessage":"Available","forkable":"true","project":{"key":"FRON","id":109,"name":"FrontEnd","description":"微前端","public":"false","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/projects/FRON"}]}},"public":"false","links":{"clone":[{"href":"https://bitbucket.pharbers.com/scm/fron/micro-frontend.git","name":"http"},{"href":"ssh://git@bitbucket.pharbers.com:7999/fron/micro-frontend.git","name":"ssh"}],"self":[{"href":"https://bitbucket.pharbers.com/projects/FRON/repos/micro-frontend/browse"}]}}},"toRef":{"id":"refs/heads/master","displayId":"master","latestCommit":"3bc767cc78a6a1b43e5c0fe6b2e798cd9543f41a","repository":{"slug":"micro-frontend","id":69,"name":"micro-frontend","description":"微前端","scmId":"git","state":"AVAILABLE","statusMessage":"Available","forkable":"true","project":{"key":"FRON","id":109,"name":"FrontEnd","description":"微前端","public":"false","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/projects/FRON"}]}},"public":"false","links":{"clone":[{"href":"https://bitbucket.pharbers.com/scm/fron/micro-frontend.git","name":"http"},{"href":"ssh://git@bitbucket.pharbers.com:7999/fron/micro-frontend.git","name":"ssh"}],"self":[{"href":"https://bitbucket.pharbers.com/projects/FRON/repos/micro-frontend/browse"}]}}},"locked":"false","author":{"user":{"name":"hbzhao","emailAddress":"hbzhao@data-pharbers.com","id":302,"displayName":"赵浩博","active":"true","slug":"hbzhao","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/users/hbzhao"}]}},"role":"AUTHOR","approved":"false","status":"UNAPPROVED"},"reviewers":[],"participants":[],"properties":{"mergeCommit":{"displayId":"1807c1802d7","id":"1807c1802d79c5ea4cb741fde898e0ef25c27683"}},"links":{"self":[{"href":"https://bitbucket.pharbers.com/projects/FRON/repos/micro-frontend/pull-requests/90"}]}}}

    lambda_handler(event=event, context=None)
