'''
通过递归的方式实现Dag的动态创建
可以通过少量代码实现替换airflow的功能
Author: AlfredYang
'''

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


'''
递归的主体函数
通过dataset的名字找到需要计算的job
args：
    datasetName： 需要计算的dataset 名字
    datasets： 整个dag中所有的数据集
    jobs： 整个dag中所有的脚本
    links： 整个dag中所有的links
    stack： 递归的结果
    alljobs： 所有遍历到的所有jobs的名字

return：
    整个dag的临时路径中，最后一个计算的数据集的名称
'''
def calDatasetPath(datasetName, datasets, jobs, links, stack, alljobs=[]):
    '''
    退出情况：
    1. dabasetName不是任何job的outputs时，弹栈
    '''
    dslst = list(filter(lambda x: x['name'] == datasetName, datasets))
    if len(dslst) != 1:
        raise Exception('Wrong Arguments: datasetName')
        return datasetName


    '''
    退出情况：
    2. 当出现一个脚本被多个job使用的时候，需要弹栈
    '''
    def calNextLevelJob(joblk, nlstack, alljobs):
        nldataset = list(filter(lambda x: x['name'] == joblk['ll']['targetName'], datasets))
        curDs = nldataset[0]
    
        # if joblk next level dslk greater than 1, should out stack, donothing for inner stack
        tmplk = list(filter(lambda x: x['ll']['targetName'] in alljobs, links))
        curDslk = list(filter(lambda x: x['ll']['sourceName'] == curDs['name'], tmplk))
        if len(curDslk) > 1:
            return datasetName

        if len(nldataset) != 1:
            raise Exception('Wrong Arguments: datasetName')
            return datasetName
        return calDatasetPath(nldataset[0]['name'], datasets, jobs, links, nlstack)
    
    
    '''
    并行后，还需要的下一次递归：
    1. 并行后还需要从共同的dataset再次进栈
    '''
    def calParalleCommonParent(paralleNames):
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
        
        if len(result) == 1:
            return result[0]
        else:
            return ""


    llst = list(filter(lambda x: x['ll']['targetName'] == datasetName, links))
    
    if len(llst) == 1:
        curJ = list(filter(lambda x: x['name'] == llst[0]['ll']['sourceName'], jobs))[0]
        stack.append(curJ)
        alljobs.append(curJ['name'])
        alljobs = list(set(alljobs))
        nldslk = list(filter(lambda x: x['ll']['targetName'] == llst[0]['ll']['sourceName'], links))
        nljoblk = dslk2joblk(nldslk, links)
        if len(nljoblk) == 1:
            return calNextLevelJob(nljoblk[0], stack, alljobs)
        elif len(nljoblk) > 1:
            cstack = deque()
            tmpDsname = []
            for iter in nljoblk:
                tstack = deque()
                tmpRes = calNextLevelJob(iter, tstack, alljobs)
                if len(tstack) > 0:
                    tmpDsname.append(tmpRes)
                    cstack.append(tstack)
            stack.append(cstack)
            # ***** 重点中的难点 ***** 
            # 并行完了还需要一层递归
            nldsname = calParalleCommonParent(tmpDsname)
            if len(nldsname) > 0:
                return calDatasetPath(nldsname, datasets, jobs, links, stack, alljobs)
            
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

