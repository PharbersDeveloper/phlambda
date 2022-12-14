
from collections import deque
from copy import deepcopy


def pathIterator(cur, stack, dags, adjustDone, prevDone):
    check = list(filter(lambda x: x["name"] == cur, dags))[0]

    if not set(check["parents"]) <= set(adjustDone):
        return

    tmpParents = list(set(check["parents"]) - set(prevDone))

    # 宽依赖
    # if len(check["parents"]) > 1:
    if len(tmpParents) > 1:
        return
    # 窄依赖，递归
    else:
        if len(check["children"]) == 1:
            stack.append(cur)
            adjustDone.append(cur)
            nextCur = check["children"][0]
            pathIterator(nextCur, stack, dags, adjustDone, prevDone)
        elif len(check["children"]) > 1:
            stack.append(cur)
            adjustDone.append(cur)
            curStack = deque()
            for nextCur in check["children"]:
                tmpStack = deque()
                pathIterator(nextCur, tmpStack, dags, adjustDone, prevDone)
                if len(tmpStack) > 0:
                    curStack.append(tmpStack)
            if len(curStack) > 0:
                stack.append(curStack)
        else:
            stack.append(cur)
            adjustDone.append(cur)
            pass


def stageIterator(dags, doneJobs):
    prevDone = deepcopy(doneJobs)
    nodes = list(filter(lambda x: set(x["parents"]) <= set(doneJobs) and not x["name"] in doneJobs, dags))
    stack = deque()
    if len(nodes) == 1:
        cur = nodes[0]["name"]
        pathIterator(cur, stack, dags, doneJobs, prevDone)
    else:
        tmpStack = deque()
        for n in nodes:
            cur = n["name"]
            pathStack = deque()
            pathIterator(cur, pathStack, dags, doneJobs, prevDone)
            tmpStack.append(pathStack)
        stack.append(tmpStack)

    allJobs = list(map(lambda x: x["name"], dags))
    return {
        "stack": stack,
        "doneJobs": list(set(doneJobs)),
        "fullfilled": set(doneJobs) == set(allJobs)
    }
