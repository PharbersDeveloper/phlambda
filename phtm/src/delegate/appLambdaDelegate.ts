
import { DBConfig, JSONAPI, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import { PostgresConf } from "../constants/common"
import { callRHandler } from "../handler/callRHandler"
import { exportsHandler } from "../handler/exportsHandler"

export default class AppLambdaDelegate {
    async exec(event: any) {
        ServerRegisterConfig([new DBConfig(PostgresConf)])
        if (event.pathParameters.type === "callR") {
            return await callRHandler(event)
        }
        if (event.pathParameters.type === "export") {
            return await exportsHandler(event)
        }
        return JSONAPI(StoreEnum.POSTGRES, event)
    }
}
