import { DBConfig, JSONAPI, ServerRegisterConfig, StoreEnum } from "phnodelayer"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            const configs = [
                new DBConfig({
                    name: StoreEnum.POSTGRES,
                    entity: "max",
                    database: "phmax",
                    user: "pharbers",
                    password: "Abcde196125",
                    host: "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
                    port: 5432,
                    poolMax: 2
                })
            ]
            ServerRegisterConfig(configs)
            return JSONAPI(StoreEnum.POSTGRES, event)
        } catch (error) {
            throw error
        }
    }
}
