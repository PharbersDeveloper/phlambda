'''
通过动态规划的方式实现Dag的动态创建 v2
可以通过少量代码实现替换airflow的功能

v1 有跨level的问题，其核心载运dag递归过程中的dataset跨level又不能真确定依赖关系
Author: AlfredYang
'''

import json


class Node:
    '''
    height 到 root 的距离
    depth 到 leaf 的距离
    '''

    def __init__(self, name, height):
        self.name = name
        self.height = height
        self.parents = []
        self.children = []


class NodeSpace:
    def __init__(self, root):
        self.nodes = []
        self.root = root
        self.nodes.append(root)

    def addNode(self, n):
        self.nodes.append(n)

    def queryNodeByName(self, name):
        lst = list(filter(lambda x: x.name == name, self.nodes))
        if len(lst) == 0:
            return None
        else:
            return lst[0]


def buildExecutionDag(datasets, jobs, links, destination, recursive=True):
    '''
    :param datasets: dag 表中的 dataset 节点，抽象的理解是一种无效 node
    :param jobs: dag 表中的 job 节点，抽象的理解是另一中有效 node
    :param links: dag 表中的 link ，抽象的理解是 dag 中的 edge
    :param destination: 开始节点，表示 dataset 中的 name 要迁移成 第一个有效的 job 节点
    :return: 一个新的 dag 只有 jobs 节点, jobs
    '''

    # destinantion 必须是 datasets 中的name
    destinationLink = list(filter(lambda x: x["ll"]["targetName"] == destination, links))[0]
    destinationJob = list(filter(lambda x: x["name"] == destinationLink["ll"]["sourceName"], jobs))[0]
    # destinationJobs = list(filter(lambda x: x["name"] == destinationLink["ll"]["sourceName"], jobs))

    destinationJobNode = Node(destinationJob["name"], 0)
    nodeSpace = NodeSpace(destinationJobNode)


    def genNextHeightSpace(n):
        dss = list(filter(lambda x: x["ll"]["targetName"] == n.name, links))
        dsNames = list(map(lambda x: x["ll"]["sourceName"], dss))
        parentLinks = list(filter(lambda x: x["ll"]["targetName"] in dsNames, links))
        parentJobNames = list(map(lambda x: x["ll"]["sourceName"], parentLinks))
        # parentJobs = list(filter(lambda x: x["name"] in parentJobNames, jobs))
        for name in parentJobNames:
            tn = nodeSpace.queryNodeByName(name)
            if tn is None:
                tn = Node(name, n.height + 1)
                nodeSpace.addNode(tn)
            else:
                tn.height = n.height + 1

            n.parents.append(tn)
            n.parents = list(set(n.parents))
            tn.children.append(n)
            tn.children = list(set(tn.children))

    
    def deepFirstSearchForJobs(nodes):
        if len(nodes) == 0:
            return

        for job in nodes:
            genNextHeightSpace(job)
            deepFirstSearchForJobs(job.parents)

    
    deepFirstSearchForJobs([destinationJobNode])
    
    if recursive:
        return {
            "dags": extractDags(nodeSpace),
            "jobs": extractAllJobs(nodeSpace),
            "doneJobs": []
        }
    else:
        return {
            "dags": extractDagsRoot(nodeSpace),
            "jobs": extractRootJob(nodeSpace),
            "doneJobs": list(set(extractAllJobs(nodeSpace)) - set(extractRootJob(nodeSpace)))
        }


def extractAllJobs(nodeSpace):
    '''
    分为两种新的便利方式，第一种顺序无关走路径便利过程
    '''
    return list(map(lambda x: x.name, nodeSpace.nodes))


def extractRootJob(nodeSpace):
    '''
    分为两种新的便利方式，第一种顺序无关走路径便利过程
    '''
    return list(map(lambda x: x.name, [nodeSpace.root]))


def extractDags(nodeSpace):
    result = []
    for node in nodeSpace.nodes:
        tmpParents = list(map(lambda x: x.name, node.parents))
        tmpChildren = list(map(lambda x: x.name, node.children))
        result.append({"name": node.name, "parents": tmpParents, "children": tmpChildren})

    return result


def extractDagsRoot(nodeSpace):
    result = []
    node = nodeSpace.root    
    tmpParents = list(map(lambda x: x.name, node.parents))
    tmpChildren = list(map(lambda x: x.name, node.children))
    result.append({"name": node.name, "parents": tmpParents, "children": tmpChildren})
    return result

