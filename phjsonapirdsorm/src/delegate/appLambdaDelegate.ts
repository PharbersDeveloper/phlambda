import { Main, PostgresConfig, RedisConfig, ServerConfig } from "phnodelayer"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        const sc = new ServerConfig("layer test", {
            pg: new PostgresConfig(
                "entry",
                "postgres",
                "faiz",
                "127.0.0.1",
                5432,
                "phtest"
            ),
            redis: new RedisConfig(
                "token",
                "",
                "",
                "127.0.0.1",
                6379,
                "0"
            )
        })
        return await Main(event, sc)
    }
}
