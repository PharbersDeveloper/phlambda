// import { identify } from "phauthlayer"
import { ConfigRegistered, Logger, Main, PostgresConfig, RedisConfig, SF, Store } from "phnodelayer"
import { PostgresqlConf } from "../common/config"
import { callRHandler } from "../handler/callRHandler"

export default class AppLambdaDelegate {
    async exec(event: Map<string, any>) {
        // @ts-ignore
        if (event.pathParameters.type === "callR") {
            return await callRHandler(event)
        }
        const postgresConf = new PostgresConfig(PostgresqlConf.entry, PostgresqlConf.user,
            PostgresqlConf.password, PostgresqlConf.url,
            PostgresqlConf.port, PostgresqlConf.db, 1, 1000 * 10, 1000 * 10)
        ConfigRegistered.getInstance.registered(postgresConf)
        return Main(event)
        // ConfigRegistered.getInstance.registered(postgresConf)
        // const dbIns = SF.getInstance.get(Store.Postgres)
        // // await dbIns.open()
        // const result = await JsonApiMain({event, db: dbIns})
        // await dbIns.close()
        // return result
    }
}
