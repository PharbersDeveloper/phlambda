import { ServerResponse } from "http"
import { AWSRequest, DBConfig, IStore, Logger, Register, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import { AccountUri, PostgresConf, RedisConf} from "../constants"
import { UnauthorizedRequestError } from "../errors"
import { LoginHandler, UserInfoHandler } from "../handlers"
import { OAuth2Server, Request, Response } from "../index"
import { Pharbers } from "../models/pharbers"

export default class AppLambdaDelegate {
    private postgres: IStore
    private redis: IStore
    async exec(event: any) {
        const paths = event.path.split("/")
        const projectName = paths[0] === "" ? paths[1] : paths[0]
        const configs = [
            new DBConfig(PostgresConf),
            new DBConfig(RedisConf)
        ]

        ServerRegisterConfig(configs)

        this.redis = Register.getInstance.getData(StoreEnum.REDIS) as IStore
        this.postgres = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
        // await this.postgres.open()
        // await this.redis.open()

        const awsRequest = new AWSRequest(event, projectName)
        const awsResponse = new ServerResponse(awsRequest)
        try {
            if (!event.body) {
                event.body = ""
            }
            const oauth = new OAuth2Server({
                model: new Pharbers()
            })

            const request = new Request(awsRequest)
            const response = new Response(awsResponse)

            const endpoint = event.pathParameters.edp
            if (endpoint === "login") {
                await new LoginHandler().handle(request, response)
            } else if (endpoint === "authorization") {
                const r = await oauth.authorize(request, response)
                const state = request.body.state || request.query.state
                const code = r.authorizationCode
                const redirectUri = r.redirectUri
                response.status = 200
                response.body = { redirectUri: `${redirectUri}?code=${code}&state=${state}` }
                return response
            } else if (endpoint === "token") {
                await oauth.token(request, response)
            }  else if (endpoint === "userinfo" || endpoint === "userInfo" || endpoint === "user_info" ) {
                await new UserInfoHandler().handle(request, response)
            }

            return response
        } catch (error) {
            if (error instanceof UnauthorizedRequestError &&
                error.message === "Unauthorized request: no authentication given") {
                const scope = "APP|*|R"
                const url = [
                    `client_id=${awsRequest.query["client_id"]}`,
                    `redirect_uri=${awsRequest.query["redirect_uri"]}`,
                    `scope=${awsRequest.query["scope"] || scope}`,
                    `state=${awsRequest.query["state"]}`
                ].join("&")
                const r = new Response(awsResponse)
                r.redirect(`${AccountUri.uri}?${url}`)
                return r
            } else {
                throw error
            }
        } finally {
            // await this.postgres.close()
            // await this.redis.close()
        }
    }
}
