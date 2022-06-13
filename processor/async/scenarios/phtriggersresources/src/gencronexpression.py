

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
        indexOfPeriod = time_attribute.index(self.period)
        map_TimeAndValue = list(zip(time_attribute, time_value))
        return map_TimeAndValue, indexOfPeriod

    def get_cron_expression(self):
        map_TimeAndValue, indexOfPeriod  = self.get_base()
        result = list(map(lambda x: x[-1] + "/1" if map_TimeAndValue.index(x) < indexOfPeriod else (x[-1] + f"/{self.period_value}" if map_TimeAndValue.index(x) == indexOfPeriod else x[-1]), map_TimeAndValue))
        cron_data = list(reversed(result))
        #-------asw event rule cron 精度为分，没有秒-------------#
        cron_expression = "cron(" + " ".join(cron_data[1:5]) + " ? " + cron_data[-1] + ")"
        print(cron_expression)
        return cron_expression
