import { ConfigRegistered, Main, PostgresConfig, RedisConfig } from "phnodelayer"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        const pg = new PostgresConfig("entry", "postgres", "faiz", "127.0.0.1", 5432, "phtest")
        const redis = new RedisConfig("token", "", "", "127.0.0.1", 6379, "0")
        ConfigRegistered.getInstance.registered(pg).registered(redis)
        return await Main(event)
    }
}
