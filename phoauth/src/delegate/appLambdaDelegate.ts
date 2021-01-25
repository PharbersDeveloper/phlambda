import { ServerResponse } from "http"
import { AWSRequest, ConfigRegistered, Logger, PostgresConfig, RedisConfig, SF, Store } from "phnodelayer"
import { AccountUri, PostgresConf, RedisConf} from "../constants"
import { UnauthorizedRequestError } from "../errors"
import {CodeResponseType, OAuth2Server, Request, Response, TokenResponseType} from "../index"
import { Pharbers } from "../models/pharbers"

// import AuthorizationHandler from "../handler_back/authorizationHandler"
// import LoginHandler from "../handler_back/loginHandler"
// import TokenHandler from "../handler_back/tokenHandler"
// import UserInfoHandler from "../handler_back/userInfoHandler"

export default class AppLambdaDelegate {
    redis: any = null
    postgres: any = null
    async exec(event: any) {
        const awsRequest = new AWSRequest(event, PostgresConf.entry)
        const awsResponse = new ServerResponse(awsRequest)
        const pg = new PostgresConfig(
            PostgresConf.entry, PostgresConf.user, PostgresConf.password,
            PostgresConf.url, PostgresConf.port, PostgresConf.db
        )
        const rds = new RedisConfig(
            RedisConf.entry, RedisConf.user, RedisConf.password,
            RedisConf.url, RedisConf.port, RedisConf.db
        )
        ConfigRegistered.getInstance.registered(pg).registered(rds)
        this.redis = SF.getInstance.get(Store.Redis)
        this.postgres = SF.getInstance.get(Store.Postgres)
        await this.postgres.open()
        await this.redis.open()
        try {
            if (!event.body) {
                event.body = ""
            }
            const oauth = new OAuth2Server({
                model: new Pharbers()
            })

            await oauth.authorize(new Request(awsRequest), new Response(awsResponse))
        } catch (error) {
            if (error instanceof UnauthorizedRequestError && error.message === "Unauthorized request: no authentication given") {
                const parm = [
                    // @ts-ignore
                    `client_id=${awsRequest.query.client_id}`,
                    // @ts-ignore
                    `redirect_uri=${awsRequest.query.redirect_uri}`,
                    // @ts-ignore
                    `scope=${awsRequest.query.scope}`,
                    // @ts-ignore
                    `state=${awsRequest.query.state}`]
                const r = new Response(awsResponse)
                r.redirect(`${AccountUri.uri}?${parm.join("&")}`)
                return r
            } else {
                throw error
            }
        } finally {
            await this.postgres.close()
            await this.redis.close()
        }
    }

    private updateResponse(response: Response,
                           redirectUri: any,
                           responseType: string,
                           state: any) {

    }
}

// export default class AppLambdaDelegate {
//     public redis: any = null
//     public postgres: any = null
//     public async exec(event: Map<string, any>) {
//         const pg = new PostgresConfig(
//             PostgresqlConf.entry,
//             PostgresqlConf.user,
//             PostgresqlConf.password,
//             PostgresqlConf.url,
//             PostgresqlConf.port,
//             PostgresqlConf.db
//         )
//         const rds = new RedisConfig(
//             RedisConf.entry,
//             RedisConf.user,
//             RedisConf.password,
//             RedisConf.url,
//             RedisConf.port,
//             RedisConf.db
//         )
//         ConfigRegistered.getInstance.registered(pg).registered(rds)
//         this.redis = SF.getInstance.get(Store.Redis)
//         this.postgres = SF.getInstance.get(Store.Postgres)
//         await this.postgres.open()
//         await this.redis.open()
//         try {
//             // @ts-ignore
//             if (!event.body) {
//                 // @ts-ignore
//                 event.body = ""
//             }
//             const req = new AWSRequest(this.convert(event), PostgresqlConf.entry)
//             const response = new ServerResponse(req)
//             // @ts-ignore
//             const endpoint = event.pathParameters.edp
//             if (endpoint === "login") {
//                 await new LoginHandler().execute(event, response, this.postgres, this.redis)
//             } else if (endpoint === "authorization") {
//                 await new AuthorizationHandler().execute(event, response, this.postgres, this.redis)
//             } else if (endpoint === "token") {
//                 await new TokenHandler().execute(event, response, this.postgres, this.redis)
//             } else if (endpoint === "userinfo") {
//                 await new UserInfoHandler().execute(event, response, this.postgres, this.redis)
//             }
//             return response
//         } catch (e) {
//             throw e
//         } finally {
//             await this.postgres.close()
//             await this.redis.close()
//         }
//     }

//     private convert(event: any): any {
//         // 目前只保证jupyter
//         if (event.httpMethod === "POST") {
//             // tslint:disable-next-line:no-unused-expression
//             if (event.headers.Authorization.indexOf("Basic") !== -1) {
//                 // tslint:disable-next-line:no-unused-expression
//                 const parm = Buffer.from(event.headers.Authorization.replace("Basic ", ""), "base64").toString().split(":")
//                 event.httpMethod = "GET"
//                 const body = `client_id=${parm[0]}&client_secret=${parm[1]}&${event.body}`
//                 event.body = ""
//                 let queryObj = {}
//                 for (const item of body.split("&")) {
//                     const obj = item.split("=")
//                     queryObj[obj[0]] = obj[1]
//                 }
//                 event.queryStringParameters = queryObj
//             }
//         }
//         return event
//     }
// }
