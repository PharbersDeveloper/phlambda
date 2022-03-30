import { LogEnum } from "../common/LogEnum"
import LogContext from "./LogContext"
import MapReduceLogsHandler from "./MapReduceLogsHandler"
import StepFunctionHandler from "./StepFunctionHandler"

export default class LogsHandler {
    private stf: StepFunctionHandler

    constructor() {
        this.stf = new StepFunctionHandler()
    }

    async getLogs(arn: string, name: string) {
        const events = (await this.stf.findEventHistory(arn)).filter((item) => item.name === name)
        const strategy = this.choiceStrategy(events)
        if (strategy) {
            return await strategy.execute()
        }
        return {}
    }

    private choiceStrategy(events: any[]) {
        const types = new Set(events.map((item) => item.resourceType).filter((item) => item !== ""))
        const logContext: LogContext = new LogContext(events)
        switch (true) {
            case types.has(LogEnum.MAPREDUCE):
                logContext.setStrategy(new MapReduceLogsHandler(process.env.AccessKeyId, process.env.SecretAccessKey))
                return logContext
            case types.has(LogEnum.LAMBDA):
                return null
            case types.has(LogEnum.GLUEJOB):
                return null
            case types.has(LogEnum.GLUECRAWLER):
                return null
        }
    }
}
