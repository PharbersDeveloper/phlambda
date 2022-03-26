import {ServerResponse} from "http"
import { AWSRequest, DBConfig, IStore, JSONAPI, Logger, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import LogsHandler from "../handler/LogsHandler"
import StepFunctionHandler from "../handler/StepFunctionHandler"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            const configs = [
                new DBConfig({
                    name: StoreEnum.POSTGRES,
                    entity: "project",
                    database: "phentry",
                    user: "pharbers",
                    password: "Abcde196125",
                    host: "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
                    port: 5432,
                    poolMax: 2
                })
            ]
            ServerRegisterConfig(configs)
            if (event.pathParameters.type === "stopexecution" && event.httpMethod.toLowerCase() === "post") {
                const stp = new StepFunctionHandler()
                const arn = JSON.parse(event.body).arn
                await stp.stopExecution(arn)
            } else if (event.pathParameters.type === "logs" && event.httpMethod.toLowerCase() === "post") {
                const paths = event.path.split("/")
                const projectName = paths[0] === "" ? paths[1] : paths[0]
                const awsRequest = new AWSRequest(event, projectName)
                const awsResponse = new ServerResponse(awsRequest)
                const body = JSON.parse(event.body)
                const result = await new LogsHandler().getLogs(body.arn, body.name)
                awsResponse["outputData"] = [{data: ""}, {data: JSON.stringify(result)}]
                return awsResponse
            } else {
                return JSONAPI(StoreEnum.POSTGRES, event)
            }
        } catch (error) {
            throw error
        }
    }
}
