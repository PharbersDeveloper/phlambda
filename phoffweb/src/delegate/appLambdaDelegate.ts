import { identify } from "phauthlayer"
import { DBConfig, IStore, JSONAPI, Logger, Register, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import { PostgresConf } from "../constants/common"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            const configs = [
                new DBConfig(PostgresConf)
            ]
            ServerRegisterConfig(configs)
            const redis = Register.getInstance.getData(StoreEnum.REDIS) as IStore
            await redis.open()
            const result = await redis.find("access", null, {match: {token: event.headers.Authorization}})
            await redis.close()
            let scope = ""
            if (result.payload.records.length > 0) {
                scope  = result.payload.records[0].scope
            }
            const flag = identify(event, scope)
            if (flag.status === 200) {
                return JSONAPI(StoreEnum.POSTGRES, event)
            }
            return flag
        } catch (error) {
            throw error
        }
    }
}
