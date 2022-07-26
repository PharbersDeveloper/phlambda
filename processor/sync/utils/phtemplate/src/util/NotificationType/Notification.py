import json
from datetime import datetime


class Notification:

    def transform_ptp(self, cat, data, project, owner, event):
        if cat == "notification":
            projectId = data[0]["projectId"]
            if "_compute_" in projectId:
                return self.__to_dag(data, project, owner, event)
            else:
                return self.__to_normal(data[0], project, owner, event)
        else:
            result = {}
            content = data[0]
            projectId, ownerId = content["id"].split("_")
            time = int(datetime.fromisoformat(content["runnerId"].split("_")[-1]).timestamp() * 1000)
            runnerId = "_".join(content["runnerId"].split("_")[:-1]) + "_" + str(time)
            jobDesc = "executionStatus" + runnerId
            if project == projectId and ownerId == owner and jobDesc == event:
                result["jobCat"] = "notification"
                result["jobDesc"] = jobDesc
                return dict(result, **content)
            return result

    def __to_dag(self, data, project, owner, event):
        def expr(item):
            message = json.loads(item["message"])
            jobDesc = item["jobDesc"]
            ownerId = message["opname"]
            projectId = item["projectId"][0:item["projectId"].index("_compute_")]
            return project == projectId and ownerId == owner

        return list(filter(expr, data))

    def __to_normal(self, data, project, owner, event):
        result = {}
        projectId = data["projectId"]
        message = json.loads(data["message"])
        jobDesc = data["jobDesc"]
        ownerId = message["opname"]
        if (project == projectId and ownerId == owner) or (project == "projectid"):
            return dict(result, **data)
        return result

    def transform_group(self, cat, data, project):
        return {}
        # result = {}
        # if cat == "notification":
        #     projectId = data["projectId"]
        #     if project == projectId:
        #         return dict(result, **data)
        #     return result
        # else:
        #     projectId = data["id"][:15]
        #     runnerId = data["runnerId"]
        #     jobDesc = "executionStatus" + runnerId
        #     if project == projectId:
        #         result["jobCat"] = "notification"
        #         result["jobDesc"] = jobDesc
        #         return dict(result, **data)
        #     return result
