



class GenCronExpression:
    def __init__(self, start_time, period, value):
        self.start_time = start_time
        self.period = period
        self.period_value = value

    def get_base(self):
        import re
        base_match_patter = r"(\d{4})-(\d{1,2})-(\d{1,2}) (\d{1,2}):(\d{1,2}):(\d{1,2})"
        time_value = re.findall(pattern=base_match_patter, string=str(self.start_time))[0]
        time_attribute = ["year", "month", "day", "hour", "minute", "second"]
        timeDict = dict(zip(time_attribute, time_value))
        return timeDict

    def get_cron_expression(self):
        timeDict = self.get_base()
        timeDict[self.period] = timeDict[self.period] + "/" + str(self.period_value)
        #-------asw event rule cron 精度为分，没有秒-------------#
        cron_data = list(reversed(timeDict.values()))
        cron_expression = "cron(" + " ".join(cron_data[1:4]) + " ? " + cron_data[-1] + ")"
        return cron_expression
