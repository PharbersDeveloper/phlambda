import json

class Parse:
    def __init__(self, *args):
        pass

    def print_branch_information(self, event):
        body = json.loads(event['body'].replace("'", "\""))
        # body = event["body"]
        if body["eventKey"] == "repo:refs_changed":
            return self.branch_change(body)
        if body["eventKey"] == "pr:merged":
            return self.branch_merge(body)

    def branch_change(self, body):
        # body = json.loads(event["body"])
        # body = event["body"]
        git_change_message = {}
        git_change_message["event_key"] = body["eventKey"]
        git_change_message["event_type"] = body["changes"][0]["type"]
        git_change_message["time"] = body["date"]
        git_change_message["operator_name"] = body["actor"]["name"]
        git_change_message["repository_name"] = body["repository"]["name"]
        git_change_message["branch_namee"] = body["changes"][0]["ref"]["displayId"]
        return git_change_message

    def branch_merge(self, body):
        # body = json.loads(event["body"])
        # body = event["body"]
        git_change_message = {}
        git_change_message["event_key"] = body["eventKey"]
        git_change_message["event_state"] = body["pullRequest"]["state"]
        git_change_message["time"] = body["date"]
        git_change_message["operator_name"] = body["actor"]["name"]
        git_change_message["merge_description"] = body["pullRequest"]["description"]
        git_change_message["merge_repository_from"] = \
            body["pullRequest"]["fromRef"]["repository"]["name"]
        git_change_message["merge_branch_from"] = body["pullRequest"]["fromRef"]["displayId"]
        git_change_message["merge_repository_to"] = body["pullRequest"]["toRef"]["repository"]["name"]
        git_change_message["merge_branch_to"] = body["pullRequest"]["toRef"]["displayId"]
        git_change_message["merge_request_user"] = body["pullRequest"]["author"]["user"]["name"]
        reviewers = []
        for reviewer in body["pullRequest"]["reviewers"]:
            reviewers.append(reviewer["user"]["name"])
        git_change_message["merge_reviewers"] = reviewers
        return git_change_message
