import { ServerResponse } from "http"
import { AWSRequest, ConfigRegistered, Logger, PostgresConfig, RedisConfig, SF, Store } from "phnodelayer"
import { PostgresqlConf, RedisConf } from "../common/config"
import AuthorizationHandler from "../handler/authorizationHandler"
import LoginHandler from "../handler/loginHandler"
import TokenHandler from "../handler/tokenHandler"
import UserInfoHandler from "../handler/userInfoHandler"

export default class AppLambdaDelegate {
    public redis: any = null
    public postgres: any = null
    public async exec(event: Map<string, any>) {
        const pg = new PostgresConfig(
            PostgresqlConf.entry,
            PostgresqlConf.user,
            PostgresqlConf.password,
            PostgresqlConf.url,
            PostgresqlConf.port,
            PostgresqlConf.db
        )
        const rds = new RedisConfig(
            RedisConf.entry,
            RedisConf.user,
            RedisConf.password,
            RedisConf.url,
            RedisConf.port,
            RedisConf.db
        )
        ConfigRegistered.getInstance.registered(pg).registered(rds)
        this.redis = SF.getInstance.get(Store.Redis)
        this.postgres = SF.getInstance.get(Store.Postgres)
        await this.postgres.open()
        await this.redis.open()
        try {
            // @ts-ignore
            if (!event.body) {
                // @ts-ignore
                event.body = ""
            }
            const req = new AWSRequest(event, PostgresqlConf.entry)
            const response = new ServerResponse(req)
            // @ts-ignore
            const endpoint = event.pathParameters.edp
            if (endpoint === "login") {
                await new LoginHandler().execute(event, response, this.postgres, this.redis)
            } else if (endpoint === "authorization") {
                await new AuthorizationHandler().execute(event, response, this.postgres, this.redis)
            } else if (endpoint === "token") {
                await new TokenHandler().execute(event, response, this.postgres, this.redis)
            } else if (endpoint === "userinfo") {
                await new UserInfoHandler().execute(event, response, this.postgres, this.redis)
            }
            return response
        } catch (e) {
            throw e
        } finally {
            await this.postgres.close()
            await this.redis.close()
        }
    }
}
