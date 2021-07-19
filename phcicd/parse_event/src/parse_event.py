import json

class Parse:
    def __init__(self, *args):
        pass

    def print_branch_information(self, event):
        if event["headers"]["X-Event-Key"] == "repo:refs_changed":
            return self.branch_change(event)
        if event["headers"]["X-Event-Key"] == "pr:merged":
            return self.branch_merge(event)

    def branch_change(self, event):
        git_change_message = {}
        git_change_message["event_key"] = json.loads(event["body"])["eventKey"]
        git_change_message["event_type"] = json.loads(event["body"])["changes"][0]["type"]
        git_change_message["time"] = json.loads(event["body"])["date"]
        git_change_message["operator_name"] = json.loads(event["body"])["actor"]["name"]
        git_change_message["repository_name"] = json.loads(event["body"])["repository"]["name"]
        git_change_message["branch_namee"] = json.loads(event["body"])["changes"][0]["ref"]["displayId"]
        return git_change_message

    def branch_merge(self, event):
        git_change_message = {}
        git_change_message["event_key"] = json.loads(event["body"])["eventKey"]
        git_change_message["event_state"] = json.loads(event["body"])["pullRequest"]["state"]
        git_change_message["time"] = json.loads(event["body"])["date"]
        git_change_message["operator_name"] = json.loads(event["body"])["actor"]["name"]
        git_change_message["merge_description"] = json.loads(event["body"])["pullRequest"]["description"]
        git_change_message["merge_repository_from"] = \
            json.loads(event["body"])["pullRequest"]["fromRef"]["repository"]["name"]
        git_change_message["merge_branch_from"] = json.loads(event["body"])["pullRequest"]["fromRef"]["displayId"]
        git_change_message["merge_repository_to"] = json.loads(event["body"])["pullRequest"]["toRef"]["repository"]["name"]
        git_change_message["merge_branch_to"] = json.loads(event["body"])["pullRequest"]["toRef"]["displayId"]
        git_change_message["merge_request_user"] = json.loads(event["body"])["pullRequest"]["author"]["user"]["name"]
        reviewers = []
        for reviewer in json.loads(event["body"])["pullRequest"]["reviewers"]:
            reviewers.append(reviewer["user"]["name"])
        git_change_message["merge_reviewers"] = reviewers
        return git_change_message
