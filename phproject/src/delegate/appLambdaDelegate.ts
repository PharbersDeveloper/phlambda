import { DBConfig, IStore, JSONAPI, Logger, ServerRegisterConfig, StoreEnum} from "phnodelayer"

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
                    host: "127.0.0.1",
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
