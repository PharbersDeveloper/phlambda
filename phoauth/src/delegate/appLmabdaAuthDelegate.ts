import axios from "axios"
import CryptoJS from "crypto-js"
import {ServerResponse} from "http"
import moment from "moment"
import {
    errors2response, PhInvalidAuthGrant,
    PhInvalidClient, PhInvalidGrantType,
    PhInvalidParameters,
    PhInvalidPassword,
    PhNotFoundError
} from "../errors/pherrors"
import phLogger from "../logger/phLogger"
import AWSReq from "../strategies/awsRequest"
import AppLambdaDelegate from "./appLambdaDelegate"

/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */
export default class AppLambdaAuthDelegate extends AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        // @ts-ignore
        if (!event.body) {
            // @ts-ignore
            event.body = ""
        }
        const req = new AWSReq(event, undefined)
        const response = new ServerResponse(req)
        // @ts-ignore
        const endpoint = event.pathParameters.edp
        if (endpoint === "login") {
            await this.loginHandler(event, response)
        } else if (endpoint === "authorization") {
            await this.authHandler(event, response)
        } else if (endpoint === "token") {
            await this.tokenHandler(event, response)
        } else if (endpoint === "callback") {
            await this.callbackFunc(event, response)
        }
        return response
    }

    protected async loginHandler(event: Map<string, any>, response: ServerResponse) {
        // @ts-ignore
        // const body = JSON.parse(event.body)
        // @ts-ignore
        const email = event.queryStringParameters.email
        // @ts-ignore
        const result = await this.store.find("account", null, { match: { email } } )
        // const response = {}
        if (result.payload.records.length === 0) {
            errors2response(PhNotFoundError, response)
            return response
        } else if (result.payload.records.length === 1) {

            const account = result.payload.records[0]
            // @ts-ignore
            if (account.password === event.queryStringParameters.password) {
                // @ts-ignore
                response.statusCode = 200
                // @ts-ignore
                response.headers = { "Content-Type": "application/json", "Accept": "application/json" }
                const record = result.payload.records[0]
                // @ts-ignore
                response.body = { message: "login success", uid: record.id }
            } else {
                errors2response(PhInvalidPassword, response)
            }

        } else {
            errors2response(PhNotFoundError, response)
        }

        phLogger.info(response)
        return response
    }

    /**
     * Authorization endpoint - used by the client to obtain
     * authorization from the resource owner via user-agent redirection.
     * @param event
     *        the parameters include
     *          response_type REQUIRED.  Value MUST be set to "code".
     *          client_id REQUIRED.  The client identifier as described in Section 2.2.
     *          redirect_uri OPTIONAL.
     *          scope OPTIONAL.  The scope of the access request as described by
     *          state RECOMMENDED.  An opaque value used by the client to maintain
     *              state between the request and callback.  The authorization
     *              server includes this value when redirecting the user-agent back
     *              to the client.
     *          user_id REQUIRED.  The user identifier as described in Section 2.2.
     * @param response handler http response
     */
    protected async authHandler(event: Map<string, any>, response: ServerResponse) {
        // @ts-ignore
        const redirectUri = event.queryStringParameters.redirect_uri // 重定向
        // @ts-ignore
        const responseType = event.queryStringParameters.response_type // code?
        if (responseType !== "code") {
            errors2response(PhInvalidParameters, response)
            return response
        }
        // @ts-ignore
        const clientId = event.queryStringParameters.client_id // client 是干啥的
        // @ts-ignore
        const client = await this.store.find("client", clientId)
        const clientRecord = client.payload.records[0]
        if (clientRecord.expired !== null && clientRecord.expired < new Date()) {
            errors2response(PhInvalidClient, response)
            return response
        }
        const clientName = clientRecord.name

        // @ts-ignore
        let scope = event.queryStringParameters.scope // 不同前端项目对应不同的client和scope
        if (scope === undefined) {
            scope = ["APP", clientName, "R"].join("|")
        }

        // @ts-ignore
        const userId = event.queryStringParameters.user_id
        const account = await this.store.find("account", userId, null, ["defaultRole", "scope"])
        const scopeRecord = account.payload.include.scope.map((x) => x.scopePolicy)
        if (!this.grantScopeAuth(scope, scopeRecord)) {
            errors2response(PhInvalidAuthGrant, response)
            return response
        }

        // @ts-ignore
        let state = event.queryStringParameters.state
        if (state === null || state === undefined) {
            state = "xyz"
        }

        // 需要返回一个url

        // @ts-ignore
        response.statusCode = 200
        if (redirectUri) {
            // @ts-ignore
            response.body = "code=" + await this.genAuthCode(userId, clientId, scope) + "&redirect_uri=" + redirectUri + "&state=" + state
        } else {
            // @ts-ignore
            response.body = "code=" + await this.genAuthCode(userId, clientId, scope) + "&state=" + state
        }
        // @ts-ignore
        response.headers = { "Content-Type": "application/x-www-form-urlencoded" }
        return response
    }

    /**
     * token endpoint
     * @param event
     *        the parameters include
     *          grant_type REQUIRED.  Value MUST be set to "authorization_code".
     *          code REQUIRED.  The authorization code received from the authorization server.
     *          redirect_uri. REQUIRED, if the "redirect_uri" parameter was included in the
     *                        authorization request as described in Section 4.1.1, and their
     *                        values MUST be identical.
     *          client_id REQUIRED, if the client is not authenticating with the
     *                        authorization server as described in Section 3.2.1.
     * @param response handler http response
     */
    protected async tokenHandler(event: Map<string, any>, response: ServerResponse) {
        // @ts-ignore
        const redirectUri = event.queryStringParameters.redirect_uri
        // @ts-ignore
        const clientId = event.queryStringParameters.client_id
        // @ts-ignore
        const code = event.queryStringParameters.code
        // @ts-ignore
        const grantType = event.queryStringParameters.grant_type

        if (grantType !== "authorization_code") {
            errors2response(PhInvalidGrantType, response)
            return response
        }

        const codeRecord = await this.store.find("authorization", null, { match: { code }})
        const content = codeRecord.payload.records[0]
        if (content) {
            phLogger.info(content)

            // TODO: Check register redirect URI
            // if (content.redirectUri !== redirectUri ||
            //     content.clientId !== clientId) {
            //     errors2response(PhInvalidParameters, response)
            //     return response
            // }

            const accessToken = await this.genAccessToken(clientId)

            // @ts-ignore
            response.statusCode = 200
            // @ts-ignore
            response.headers = { "Content-Type": "application/json" }
            // @ts-ignore
            response.body = {
                access_token: accessToken.token,
                token_type: "bearer",
                expires_in: 64800,
                refresh_token: accessToken.refresh,
            }
            return response
        } else {
            errors2response(PhInvalidParameters, response)
            return response
        }
    }

    // TODO: 暂时验证第一个
    protected grantScopeAuth(scope: string, policies: string[]) {
        const policy = policies[0]
        if (policy === "*") {
            return true
        }

        // TODO: check account scope
    }

    protected async genAuthCode(uid: string, cid: string, scope: string) {
        const exp = moment(new Date()).add(10, "m").toDate()
        const code = this.hexEncode(this.hash(uid + cid + new Date().toISOString() + Math.random().toString()))
        // TODO: save code to db, need to move to redis
        const authCode =  { uid, cid, code, scope, create: new Date(), expired: exp }
        await this.store.create("authorization", authCode)
        return code
    }

    protected async genAccessToken(cid: string) {
        const exp = moment(new Date()).add(1, "week").toDate()
        const accessToken = this.hexEncode(this.hash(cid + new Date().toISOString() + Math.random().toString()))
        // const refreshToken = this.hexEncode(this.hash(cid + new Date().toISOString() + Math.random().toString()))
        // TODO: save access_token to db, need to move to redis
        const tk = { cid, token: accessToken, refresh: accessToken, create: new Date(), expired: exp }
        await this.store.create("access", tk)
        return tk
    }

    protected async callbackFunc(event: Map<string, any>, response: ServerResponse) {
        // @ts-ignore
        const redirectUri = event.queryStringParameters.redirect_uri
        // TODO: Check redirectUri
        // @ts-ignore
        const clientId = "V5I67BHIRVR2Z59kq-a-"
        // @ts-ignore
        const code = event.queryStringParameters.code
        const url = "callback?grant_type=authorization_code&code=" + code + "&&redirect_uri=" + redirectUri

        const tokenResult = await axios.get("https://2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn/v0/" + url)
        phLogger.info("alfred callback test")
        phLogger.info(tokenResult)
        phLogger.info("alfred callback end")
        return tokenResult
    }

    protected hexEncode(value) {
        return value.toString(CryptoJS.enc.Hex)
    }

    protected hmac(secret, value) {
        return CryptoJS.HmacSHA256(value, secret, {asBytes: true})
    }

    protected hash(value) {
        return CryptoJS.SHA256(value)
    }
}
