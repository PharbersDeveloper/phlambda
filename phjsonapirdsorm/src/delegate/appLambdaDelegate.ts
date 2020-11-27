import { ConfigRegistered, Main, PostgresConfig, RedisConfig } from "phnodelayer"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        const pg = new PostgresConfig("common", "pharbers", "Abcde196125", "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn", 5432, "phcommon")
        // tslint:disable-next-line:max-line-length
        // const redis = new RedisConfig("token", "", "", "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn", 6379, "0")
        ConfigRegistered.getInstance.registered(pg)
        return await Main(event)
    }
}
