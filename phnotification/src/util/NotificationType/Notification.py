import json


class Notification:

    @staticmethod
    def transform_ptp(cat, data, project, owner, event):
        result = {}
        if cat == "notification":
            message = json.loads(data["message"])
            jobDesc = data["jobDesc"]
            projectId = data["projectId"]
            ownerId = message["opname"]
            if project == projectId and ownerId == owner and jobDesc == event:
                return dict(result, **data)
            return result
        else:
            projectId = data["id"][:15]
            ownerId = data["id"][16:]
            runnerId = data["runnerId"]
            jobDesc = "executionStatus" + runnerId
            if project == projectId and ownerId == owner and jobDesc == event:
                result["jobCat"] = "notification"
                result["jobDesc"] = jobDesc
                return dict(result, **data)
            return result

    @staticmethod
    def transform_group(cat, data, project):
        result = {}
        if cat == "notification":
            projectId = data["projectId"]
            if project == projectId:
                return dict(result, **data)
            return result
        else:
            projectId = data["id"][:15]
            runnerId = data["runnerId"]
            jobDesc = "executionStatus" + runnerId
            if project == projectId:
                result["jobCat"] = "notification"
                result["jobDesc"] = jobDesc
                return dict(result, **data)
            return result
