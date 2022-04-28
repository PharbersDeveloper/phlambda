import json
from collections import deque


def stack2smselect(stack, args, datasets, links):
    if len(stack) == 0:
        return

    curJ = stack.popleft()

    if type(curJ) == deque:
        for p in curJ:
            stack2smselect(p, args, datasets, links)
    else:
        selectedArgs(curJ, args, datasets, links)
        stack2smselect(stack, args, datasets, links)


def selectedArgs(curJ, args, datasets, links):
    lks = list(filter(lambda x: x['ll']['targetName'] == curJ['name'], links))
    for l in lks:
        dss = list(filter(lambda x: x['name'] == l['ll']['sourceName'], datasets))
        for d in dss:
            args.append(d['representId'])

    args.append(curJ['representId'])
