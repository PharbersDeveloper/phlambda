import {DBConfig, IStore, Logger, Register, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import { AWSRegion, PostgresConf } from "../constants/common"
import GlueHandler from "../handler/GlueHandler"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            ServerRegisterConfig([new DBConfig(PostgresConf)])
            const store = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
            // await store.open()
            const handler = new GlueHandler(store, {
                region: AWSRegion
            })
            await handler.exec(event)
            // await store.close()
        } catch (error) {
            throw error
        }
    }
}
