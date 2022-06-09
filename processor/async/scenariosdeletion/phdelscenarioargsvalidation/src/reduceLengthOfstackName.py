





def reduce_length_of_stackName(stackName):
    import re
    #----------限制字符串长度---------------------#
    if len(stackName) <= 62:
        return stackName
    else:
        data = str(stackName).split('-')
        scenario = data[0]
        projectId = data[1]
        #--------取奇数,反转，切片---------------#
        scenarioId = ''.join(reversed(str(data[2])[::2]))
        #--------取偶数-----------------#
        triggerId = str(data[3])[1::2]
        if len(data) > 4:
            timeTag = re.sub(pattern='[-:\s+.]', repl='', string=''.join(data[4:]))
            stackName = '-'.join([scenario, projectId, scenarioId, triggerId, timeTag])
        else:
            stackName = '-'.join([scenario, projectId, scenarioId, triggerId])
        return reduce_length_of_stackName(stackName)
