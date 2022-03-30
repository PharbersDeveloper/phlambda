import { DBConfig, JSONAPI, Logger, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import { PostgresConf } from "../constants/common"

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
