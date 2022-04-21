import json
from collections import deque


def dslk2joblk(nldslk, links):
    result = []
    for iter in nldslk:
        nljoblk = list(filter(lambda x: x['ll']['targetName'] == iter['ll']['sourceName'], links))
        # nljoblk = list(filter(lambda x: x['ll']['sourceName'] == iter['ll']['targetName'], links))[0]
        if len(nljoblk) > 0:
            result.append(nljoblk[0])
    return result


def calDatasetPathOne(datasetName, datasets, jobs, links, stack):
    dslst = list(filter(lambda x: x['name'] == datasetName, datasets))
    if len(dslst) != 1:
        print(datasetName)
        raise Exception('Wrong Arguments: datasetName')
        return False


    llst = list(filter(lambda x: x['ll']['targetName'] == datasetName, links))
    if len(llst) == 1:
        # stack.append(llst[0])
        curJ = list(filter(lambda x: x['name'] == llst[0]['ll']['sourceName'], jobs))[0]
        stack.append(curJ)
        nldslk = list(filter(lambda x: x['ll']['targetName'] == llst[0]['ll']['sourceName'], links))
        nljoblk = dslk2joblk(nldslk, links)
        if len(nljoblk) == 1:
            pass
            # calNextLevelJob(nljoblk[0], stack)
        elif len(nljoblk) > 1:
            cstack = deque()
            for iter in nljoblk:
                tstack = deque()
                # tmpJ = list(filter(lambda x: x['name'] == iter['ll']['sourceName'], jobs))[0]
                # tstack.append(tmpJ)
                # calNextLevelJob(iter, tstack)
                cstack.append(tstack)
            stack.append(cstack)
        else:
            # 递归退出逻辑
            pass

    return True


def calDatasetPath(datasetName, datasets, jobs, links, stack):
    dslst = list(filter(lambda x: x['name'] == datasetName, datasets))
    if len(dslst) != 1:
        print(datasetName)
        raise Exception('Wrong Arguments: datasetName')
        return False

    curDs = dslst[0]


    def calNextLevelJob(joblk, nlstack):
        nldataset = list(filter(lambda x: x['name'] == joblk['ll']['targetName'], datasets))
        if len(nldataset) != 1:
            raise Exception('Wrong Arguments: datasetName')
            return False
        calDatasetPath(nldataset[0]['name'], datasets, jobs, links, nlstack)


    llst = list(filter(lambda x: x['ll']['targetName'] == datasetName, links))
    
    if len(llst) == 1:
        # stack.append(llst[0])
        curJ = list(filter(lambda x: x['name'] == llst[0]['ll']['sourceName'], jobs))[0]
        stack.append(curJ)
        nldslk = list(filter(lambda x: x['ll']['targetName'] == llst[0]['ll']['sourceName'], links))
        nljoblk = dslk2joblk(nldslk, links)
        if len(nljoblk) == 1:
            calNextLevelJob(nljoblk[0], stack)
        elif len(nljoblk) > 1:
            cstack = deque()
            for iter in nljoblk:
                tstack = deque()
                # tmpJ = list(filter(lambda x: x['name'] == iter['ll']['sourceName'], jobs))[0]
                # tstack.append(tmpJ)
                calNextLevelJob(iter, tstack)
                cstack.append(tstack)
            stack.append(cstack)
        else:
            # 递归退出逻辑
            pass

    elif len(llst) > 1:
        raise Exception('Wrong dag: one script only have one output')
        return False
        
    else:
        # 递归退出逻辑
        pass

    return True

