import { identify } from "phauthlayer"
import { ConfigRegistered, Logger, Main, PostgresConfig, RedisConfig, SF, Store } from "phnodelayer"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        const pg = new PostgresConfig("entry", "pharbers", "Abcde196125", "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn", 5432, "phentry")
        // const redis = new RedisConfig
        // ("token", "", "", "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn", 6379, "0")
        ConfigRegistered.getInstance.registered(pg)// .registered(redis)
        // const rds = SF.getInstance.get(Store.Redis)
        // await rds.open()
        // // @ts-ignore
        // const result = await rds.find("access", null, {match: {token: event.headers.Authorization}})
        // await rds.close()
        // let scope = ""
        // if (result.payload.records.length > 0) {
        //     scope  = result.payload.records[0].scope
        // }
        // const flag = identify(event, scope)
        // if (flag.status === 200) {
        //     return await Main(event)
        // }
        // return flag
        return await Main(event)
    }
}
