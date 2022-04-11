import { Logger } from "phnodelayer"
import IStrategy from "../common/IStrategy"

export default class LambdaLogsHandler implements IStrategy {
    async extractLog(events: any[]) {
        Logger.info("Lambda Logs")
    }
}
