import { DBConfig, IStore, JSONAPI, Logger, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import PagePartitionHandler from "../handler/PagePartitionHandler"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            const endpoint = event.pathParameters.type
            const configs = [
                new DBConfig({
                    name: StoreEnum.POSTGRES,
                    entity: "catlog",
                    database: "phentry",
                    user: "pharbers",
                    password: "Abcde196125",
                    host: "127.0.0.1",
                    port: 5432,
                    poolMax: 2
                })
            ]
            if (endpoint === "partitions") {
                return await new PagePartitionHandler().pageFind("phdatacat", "factor", "")
            }
            ServerRegisterConfig(configs)
            return JSONAPI(StoreEnum.POSTGRES, event)
        } catch (error) {
            throw error
        }
    }
}
