// import { identify } from "phauthlayer"
import { ConfigRegistered, JsonApiMain, Logger, PostgresConfig, RedisConfig, SF, Store } from "phnodelayer"
import { PostgresqlConf } from "../common/config"

export default class AppLambdaDelegate {
    async exec(event: Map<string, any>) {
        const postgresConf = new PostgresConfig(PostgresqlConf.entry, PostgresqlConf.user,
            PostgresqlConf.password, PostgresqlConf.url,
            PostgresqlConf.port, PostgresqlConf.db)
        ConfigRegistered.getInstance.registered(postgresConf)
        const dbIns = SF.getInstance.get(Store.Postgres)
        // await dbIns.open()
        const result = await JsonApiMain({event, db: dbIns})
        await dbIns.close()
        return result
    }
}
