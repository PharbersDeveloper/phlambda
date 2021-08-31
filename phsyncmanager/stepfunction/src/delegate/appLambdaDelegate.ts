import { DBConfig, Logger, ServerRegisterConfig, StoreEnum} from "phnodelayer"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            const configs = [
                new DBConfig({
                    name: StoreEnum.POSTGRES,
                    entity: "index",
                    database: "phentry",
                    user: "pharbers",
                    password: "Abcde196125",
                    host: "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
                    port: 5432,
                    poolMax: 2
                })
            ]
            ServerRegisterConfig(configs)
        } catch (error) {
            throw error
        }
    }
}
