import {DBConfig, IStore, Logger, Register, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import { AWSRegion, PostgresConf } from "../constants/common"
import StepFunctionHandler from "../handler/StepFunctionHandler"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            ServerRegisterConfig([new DBConfig(PostgresConf)])
            const store = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
            const handler = new StepFunctionHandler(store, {
                region: AWSRegion
            })
            await handler.exec(event)
        } catch (error) {
            throw error
        }
    }
}
