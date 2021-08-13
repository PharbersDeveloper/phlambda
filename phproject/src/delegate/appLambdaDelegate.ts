import { DBConfig, IStore, JSONAPI, Logger, ServerRegisterConfig, StoreEnum} from "phnodelayer"
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
            }
            return JSONAPI(StoreEnum.POSTGRES, event)
        } catch (error) {
            throw error
        }
    }
}
