import json

class Parse:
    def __init__(self, *args):
        pass

    def print_branch_information(self, event):
        body = json.loads(event['body'].replace("'", "\""))
        # body = event["body"]
        # body = event
        if body["eventKey"] == "repo:refs_changed":
            return self.branch_change(body)
        if body["eventKey"] == "pr:merged":
            return self.branch_merge(body)

    def branch_change(self, body):
        git_change_message = {}
        git_change_message["event_key"] = body["eventKey"]
        git_change_message["event_type"] = body["changes"][0]["type"]
        git_change_message["time"] = body["date"]
        git_change_message["operator_name"] = body["actor"]["name"]
        git_change_message["repository_name"] = body["repository"]["name"]
        git_change_message["branch_name"] = body["changes"][0]["ref"]["displayId"]
        print(git_change_message)
        return git_change_message

    def branch_merge(self, body):
        git_change_message = {}
        git_change_message["event_key"] = body["eventKey"]
        git_change_message["event_type"] = body["pullRequest"]["state"]
        git_change_message["time"] = body["date"]
        git_change_message["operator_name"] = body["actor"]["name"]
        git_change_message["merge_repository_from"] = \
            body["pullRequest"]["fromRef"]["repository"]["name"]
        git_change_message["merge_branch_from"] = body["pullRequest"]["fromRef"]["displayId"]
        git_change_message["merge_repository_to"] = body["pullRequest"]["toRef"]["repository"]["name"]
        git_change_message["merge_branch_to"] = body["pullRequest"]["toRef"]["displayId"]
        git_change_message["merge_request_user"] = body["pullRequest"]["author"]["user"]["name"]
        git_change_message["git_commit_version"] = body["pullRequest"]["properties"]["mergeCommit"]["displayId"]
        reviewers = []
        for reviewer in body["pullRequest"]["reviewers"]:
            reviewers.append(reviewer["user"]["name"])
        git_change_message["merge_reviewers"] = reviewers
        return git_change_message

if __name__ == '__main__':
    evnet = {"eventKey":"pr:merged","date":"2021-11-02T10:58:28+0800","actor":{"name":"Alfred","emailAddress":"alfredyang@pharbers.com","id":70,"displayName":"杨渊","active":"true","slug":"alfred","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/users/alfred"}]}},"pullRequest":{"id":118,"version":2,"title":"Feature/PBDP-2139 excel schema apiv2","description":"* Excel预览基本迁移到apiv2上\r\n* 更新返回值加入跨域信息\r\n* 修改挂载点","state":"MERGED","open":"fasle","closed":"true","createdDate":1635763433000,"updatedDate":1635821908000,"closedDate":1635821908000,"fromRef":{"id":"refs/heads/feature/PBDP-2139-excel-schema-apiv2","displayId":"feature/PBDP-2139-excel-schema-apiv2","latestCommit":"df25cdaf15630ec5c9dab2075b8d5c2bed1cb01f","repository":{"slug":"phlambda","id":13,"name":"phlambda","scmId":"git","state":"AVAILABLE","statusMessage":"Available","forkable":"true","project":{"key":"LGC","id":25,"name":"logic","description":"业务逻辑层","public":"fasle","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC"}]}},"public":"fasle","links":{"clone":[{"href":"https://bitbucket.pharbers.com/scm/lgc/phlambda.git","name":"http"},{"href":"ssh://git@bitbucket.pharbers.com:7999/lgc/phlambda.git","name":"ssh"}],"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC/repos/phlambda/browse"}]}}},"toRef":{"id":"refs/heads/developer","displayId":"developer","latestCommit":"97049b107d823da85fec3e7b3b3552ea7214a6cb","repository":{"slug":"phlambda","id":13,"name":"phlambda","scmId":"git","state":"AVAILABLE","statusMessage":"Available","forkable":"true","project":{"key":"LGC","id":25,"name":"logic","description":"业务逻辑层","public":"fasle","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC"}]}},"public":"fasle","links":{"clone":[{"href":"https://bitbucket.pharbers.com/scm/lgc/phlambda.git","name":"http"},{"href":"ssh://git@bitbucket.pharbers.com:7999/lgc/phlambda.git","name":"ssh"}],"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC/repos/phlambda/browse"}]}}},"locked":"fasle","author":{"user":{"name":"Alex","emailAddress":"pqian@pharbers.com","id":52,"displayName":"钱鹏","active":"true","slug":"alex","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/users/alex"}]}},"role":"AUTHOR","approved":"fasle","status":"UNAPPROVED"},"reviewers":[{"user":{"name":"Alfred","emailAddress":"alfredyang@pharbers.com","id":70,"displayName":"杨渊","active":"true","slug":"alfred","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/users/alfred"}]}},"lastReviewedCommit":"df25cdaf15630ec5c9dab2075b8d5c2bed1cb01f","role":"REVIEWER","approved":"true","status":"APPROVED"}],"participants":[],"properties":{"mergeCommit":{"displayId":"c3539ea01ec","id":"c3539ea01ec4bcd8c075cd024b42738d3a4a0b9a"}},"links":{"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC/repos/phlambda/pull-requests/118"}]}}}

    parse = Parse()
    res = parse.print_branch_information(event=evnet)
    print(res)