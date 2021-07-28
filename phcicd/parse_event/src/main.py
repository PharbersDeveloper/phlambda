import json
import os
from parse_event import Parse
from git_python import GitRepository

def lambda_handler(event, context):
    parse = Parse()
    print(event)
    git_event = parse.print_branch_information(event=event)
    if git_event['event_type'] == "UPDATE":
        git_url = 'https://hbzhao:123456@bitbucket.pharbers.com/scm/lgc/phlambda.git'
        local_path_prefix = '/home/hbzhao/PycharmProjects/pythonProject/phlambda/phcicd/parse_event/src'
        local_path = os.path.join(local_path_prefix, 'phlambda')
        repo = GitRepository(local_path, git_url, branch='feature/PBDP-1767-phlambda-cicd')
        print(repo.branches())

    return {
        "statusCode": 200,
        "body": json.dumps("Hello from Lambda")
    }


if __name__ == "__main__":
    add_event = {
  "body": {
    "eventKey": "repo:refs_changed",
    "date": "2021-07-28T10:19:58+0800",
    "actor": {
      "name": "hbzhao",
      "emailAddress": "hbzhao@data-pharbers.com",
      "id": "302",
      "displayName": "赵浩博",
      "active": "true",
      "slug": "hbzhao",
      "type": "NORMAL",
      "links": {
        "self": [
          {
            "href": "https://bitbucket.pharbers.com/users/hbzhao"
          }
        ]
      }
    },
    "repository": {
      "slug": "phlambda",
      "id": "13",
      "name": "phlambda",
      "scmId": "git",
      "state": "AVAILABLE",
      "statusMessage": "Available",
      "forkable": "true",
      "project": {
        "key": "LGC",
        "id": "25",
        "name": "logic",
        "description": "业务逻辑层",
        "public": "false",
        "type": "NORMAL",
        "links": {
          "self": [
            {
              "href": "https://bitbucket.pharbers.com/projects/LGC"
            }
          ]
        }
      },
      "public": "false",
      "links": {
        "clone": [
          {
            "href": "https://bitbucket.pharbers.com/scm/lgc/phlambda.git",
            "name": "http"
          },
          {
            "href": "ssh://git@bitbucket.pharbers.com:7999/lgc/phlambda.git",
            "name": "ssh"
          }
        ],
        "self": [
          {
            "href": "https://bitbucket.pharbers.com/projects/LGC/repos/phlambda/browse"
          }
        ]
      }
    },
    "changes": [
      {
        "ref": {
          "id": "refs/heads/feature/PBDP-1767-phlambda-cicd",
          "displayId": "feature/PBDP-1767-phlambda-cicd",
          "type": "BRANCH"
        },
        "refId": "refs/heads/feature/PBDP-1767-phlambda-cicd",
        "fromHash": "d3b834dff36c15bbf6987d9393552f5a7ecd4fe6",
        "toHash": "0b1645045b22c2764687aa15d32e00162a046e6b",
        "type": "UPDATE"
      }
    ]
  }
}

    lambda_handler(event=add_event, context=None)
