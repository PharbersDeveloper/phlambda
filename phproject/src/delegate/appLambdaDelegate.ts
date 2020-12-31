import { identify } from "phauthlayer"
import { ConfigRegistered, Logger, Main, PostgresConfig, RedisConfig, SF, Store } from "phnodelayer"
import { PostgresqlConf, RedisConf } from "../common/config"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        const pg = new PostgresConfig(
            PostgresqlConf.entry, PostgresqlConf.user,
            PostgresqlConf.password, PostgresqlConf.url,
            PostgresqlConf.port, PostgresqlConf.db)
        const redis = new RedisConfig(
            RedisConf.entry, RedisConf.user,
            RedisConf.password, RedisConf.url,
            RedisConf.port, RedisConf.db)
        ConfigRegistered.getInstance.registered(pg).registered(redis)
        const rds = SF.getInstance.get(Store.Redis)
        await rds.open()
        // @ts-ignore
        const result = await rds.find("access", null, {match: {token: event.headers.Authorization}})
        await rds.close()
        let scope = ""
        if (result.payload.records.length > 0) {
            scope  = result.payload.records[0].scope
        }
        const flag = identify(event, scope)
        if (flag.status !== 200) {
            return flag
        }
        return await Main(event)
    }
}
