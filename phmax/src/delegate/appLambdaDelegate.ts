import { DBConfig, JSONAPI, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import { PostgresConf } from "../constants/common"
import LambdaHandler from "../handler/LambdaHandler"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            ServerRegisterConfig([ new DBConfig(PostgresConf) ])
            return JSONAPI(StoreEnum.POSTGRES, event)
        } catch (error) {
            throw error
        }
    }
}
