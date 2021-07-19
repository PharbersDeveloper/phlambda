import { ConfigRegistered, Logger, Main, PostgresConfig, RedisConfig, SF, Store } from "phnodelayer"
import { PostgresqlConf } from "../common/config"
import { callRHandler } from "../handler/callRHandler"
import { exportsHandler } from "../handler/exportsHandler"

export default class AppLambdaDelegate {
    async exec(event: Map<string, any>) {
        const postgresConf = new PostgresConfig(PostgresqlConf.entry, PostgresqlConf.user,
            PostgresqlConf.password, PostgresqlConf.url,
            PostgresqlConf.port, PostgresqlConf.db, 1, 1000 * 10, 1000 * 10)
        ConfigRegistered.getInstance.registered(postgresConf)
        // @ts-ignore
        if (event.pathParameters.type === "callR") {
            return await callRHandler(event)
        }
        // @ts-ignore
        if (event.pathParameters.type === "export") {
            return await exportsHandler(event)
        }
        return Main(event)
    }
}
