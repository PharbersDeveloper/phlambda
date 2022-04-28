import json
from collections import deque


def dslk2joblk(nldslk, links):
    result = []
    for iter in nldslk:
        nljoblk = list(filter(lambda x: x['ll']['targetName'] == iter['ll']['sourceName'], links))
        if len(nljoblk) > 0:
            result.append(nljoblk[0])
    return result


def calDatasetPathOne(datasetName, datasets, jobs, links, stack):
    dslst = list(filter(lambda x: x['name'] == datasetName, datasets))
    if len(dslst) != 1:
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
        raise Exception('Wrong Arguments: datasetName')
        return datasetName

    # curDs = dslst[0]
    # print("============> alfredtest ds")
    # print(curDs)
    
    # # if joblk next level dslk greater than 1, should out stack, donothing for inner stack
    # curDslk = list(filter(lambda x: x['ll']['sourceName'] == curDs['name'], links))
    # if len(curDslk) > 1:
    #     return datasetName
    # print("============> alfredtest dslk")
    # print(curDslk)
    # print(datasetName)


    def calNextLevelJob(joblk, nlstack):
        nldataset = list(filter(lambda x: x['name'] == joblk['ll']['targetName'], datasets))
        curDs = nldataset[0]
    
        # if joblk next level dslk greater than 1, should out stack, donothing for inner stack
        curDslk = list(filter(lambda x: x['ll']['sourceName'] == curDs['name'], links))
        if len(curDslk) > 1:
            return datasetName

        if len(nldataset) != 1:
            raise Exception('Wrong Arguments: datasetName')
            return datasetName
        return calDatasetPath(nldataset[0]['name'], datasets, jobs, links, nlstack)
    
    
    def calParalleCommonParent(paralleNames):
        # curDslk = list(filter(lambda x: x['ll']['sourceName'] == curDs['name'], links))
        res = []
        for name in paralleNames:
            dslk = list(filter(lambda x: x['ll']['targetName'] == name, links))
            if len(dslk) == 0:
                break
            
            curDs = dslk[0]
            joblk = list(filter(lambda x: x['ll']['targetName'] == curDs['ll']['sourceName'], links))
            if len(dslk) != 1:
                break
            
            res.append(joblk[0]['ll']['sourceName'])
        
        result = list(set(res))
        print('alfredtest =========> paralle')
        print(result)
        
        if len(result) == 1:
            return result[0]
        else:
            return ""


    llst = list(filter(lambda x: x['ll']['targetName'] == datasetName, links))
    
    if len(llst) == 1:
        # stack.append(llst[0])
        curJ = list(filter(lambda x: x['name'] == llst[0]['ll']['sourceName'], jobs))[0]
        stack.append(curJ)
        nldslk = list(filter(lambda x: x['ll']['targetName'] == llst[0]['ll']['sourceName'], links))
        nljoblk = dslk2joblk(nldslk, links)
        if len(nljoblk) == 1:
            return calNextLevelJob(nljoblk[0], stack)
        elif len(nljoblk) > 1:
            cstack = deque()
            tmpDsname = []
            for iter in nljoblk:
                tstack = deque()
                tmpRes = calNextLevelJob(iter, tstack)
                if len(tstack) > 0:
                    tmpDsname.append(tmpRes)
                    cstack.append(tstack)
            stack.append(cstack)
            # 并行完了还需要一层递归
            nldsname = calParalleCommonParent(tmpDsname)
            if len(nldsname) > 0:
                return calDatasetPath(nldsname, datasets, jobs, links, stack)
            
        else:
            # 递归退出逻辑
            pass

    elif len(llst) > 1:
        raise Exception('Wrong dag: one script only have one output')
        return datasetName
        
    else:
        # 递归退出逻辑
        pass

    return datasetName

