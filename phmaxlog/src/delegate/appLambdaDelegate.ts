import {DBConfig, IStore, Logger, Register, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import { PostgresConf } from "../constants/common"
import MaxLogHandler from "../handler/MaxLogHandler"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            ServerRegisterConfig([new DBConfig(PostgresConf)])
            const store = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
            await store.open()
            const handler = new MaxLogHandler(store)
            await handler.exec(event)
            await store.close()
        } catch (error) {
            throw error
        }
    }
}
