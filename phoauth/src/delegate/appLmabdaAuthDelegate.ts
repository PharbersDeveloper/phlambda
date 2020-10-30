import CryptoJS from "crypto-js"
import fortune from "fortune"
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

    public redisStore: any

    public async prepare() {
        await super.prepare()
        const record = this.genTokenRecord()
        const adapter = this.genRedisAdapter()
        this.redisStore = fortune(record, {adapter})
        await this.redisStore.connect()
    }

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
        } else if (endpoint === "getUserInfo") {
            return await this.getUserInfo(event, response)
        }
        return response
    }

    protected genTokenRecord() {
        const filename = "../models/token.js"
        return require(filename).default
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

        scope = this.mappingPolices(scope, scopeRecord)

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

        const codeRecord = await this.redisStore.find("authorization", null, { match: { code }})
        const content = codeRecord.payload.records[0]
        if (content) {
            phLogger.info(content)

            // TODO: Check register redirect URI
            // if (content.redirectUri !== redirectUri ||
            //     content.clientId !== clientId) {
            //     errors2response(PhInvalidParameters, response)
            //     return response
            // }
            const accessToken = await this.genAccessToken(content.uid, clientId, content.scope)

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
                uid: accessToken.uid
            }
            return response
        } else {
            errors2response(PhInvalidParameters, response)
            return response
        }
    }

    protected async getUserInfo(event: Map<string, any>, response: ServerResponse) {
        // @ts-ignore
        const token = event.queryStringParameters.token
        const result = await this.redisStore.find("access", null, { match: { token } })
        const tokenRecords = result.payload.records
        if ( tokenRecords.length === 0 ) {
            errors2response(PhInvalidParameters, response)
            return response
        }
        const uid = tokenRecords[0].uid

        // @ts-ignore
        event.resource = "/{type}/{id}"
        // @ts-ignore
        event.path = "/oauth/accounts/" + uid
        // @ts-ignore
        delete event.queryStringParameters.token
        // @ts-ignore
        event.queryStringParameters.type = "accounts"
        // @ts-ignore
        event.queryStringParameters.id = uid
        // @ts-ignore
        event.requestContext.resourcePath = "/{type}/{id}"
        // @ts-ignore
        event.requestContext.path = "/oauth/accounts/" + uid

        const res = await super.exec(event)

        // @ts-ignore
        const headersOutput = res.output[0].split("\r\n")
        const objHeader = {}
        for (const item of headersOutput) {
            const element = item.split(":")
            if (element.length === 2) {
                objHeader[element[0]] = element[1]
            }
        }
        // @ts-ignore
        response.statusCode = res.statusCode
        // @ts-ignore
        response.headers = objHeader
        // @ts-ignore
        response.body = JSON.parse(String(res.output[1]))
        return response
    }

    protected grantScopeAuth(scope: string, policies: string[]) {
        if (policies.length === 0) { return false } // 无任何权限
        if (policies.length === 1 && policies[0] === "*") { // 权限为admin
            return true
        }
        if (scope === "offwebLogin") { return true } // 官网登入，直接放行，交由后续的mapping policies设置该账户可使用权限
        const sa = scope.split("|")
        const plc = policies.map((item) => {
            const is = item.split("|")
            return {
                client: is[0],
                resource: is[1],
                permissions: is[2]
            }
        })

        // 拥有指定资源或所有资源
        const contains = plc.find((item) =>
            sa[0] === item.client && (item.resource.indexOf(sa[1]) !== -1 || item.resource === "*"))
        if (contains === undefined) {// 申请的资源不再数据库中
            return false
        }
        if (contains.permissions === "A") { return true } // 权限为A，scope权限申请，放行
        if ((sa[2] === "R" && contains.permissions !== "R")) { // 权限为W|X，scope申请为R，放行
            return true
        } else { return contains.permissions === sa[2] } // 权限为W|X，申请权限必须与预期相等
    }

    protected async genAuthCode(uid: string, cid: string, scope: string) {
        const time = 2
        const exp = moment(new Date()).add(time, "m").toDate()
        const code = this.hexEncode(this.hash(uid + cid + new Date().toISOString() + Math.random().toString()))
        // TODO: save code to db, need to move to redis
        const authCode = { uid, cid, code, scope, create: new Date(), expired: exp }
        const result = await this.redisStore.create("authorization", authCode)
        const seconds = (authCode.expired.getTime() - authCode.create.getTime()) / 1000
        // tslint:disable-next-line:max-line-length
        await this.setRedisExpire(`authorization:${result.payload.records[0].id}`, seconds.toFixed(0), JSON.stringify(result.payload.records[0]))
        return code
    }

    protected async genAccessToken(uid: string, cid: string, scope: string) {
        const time = 1
        const exp = moment(new Date()).add(time, "week").toDate()
        const accessToken = this.hexEncode(this.hash(cid + new Date().toISOString() + Math.random().toString()))
        // const refreshToken = this.hexEncode(this.hash(cid + new Date().toISOString() + Math.random().toString()))
        const tk = { uid, cid, token: accessToken, refresh: accessToken, create: new Date(), expired: exp, scope }
        const result = await this.redisStore.create("access", tk)
        const seconds = (tk.expired.getTime() - tk.create.getTime()) / 1000
        // tslint:disable-next-line:max-line-length
        await this.setRedisExpire(`access:${result.payload.records[0].id}`, seconds.toFixed(0), JSON.stringify(result.payload.records[0]))
        return tk
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

    protected async setRedisExpire(key, expire, value) {
        return await this.redisStore.adapter.redis.set(key, value, "EX", expire)
    }

    protected mappingPolices(scope: string, policies: string[]) {
        if (policies.length === 1 && policies[0] === "*") { // 权限为admin
            return "*"
        }
        // @ts-ignore
        let sp
        const plc = policies.map((item: string) => {
            const is = item.split("|")
            return {
                client: is[0],
                resource: is[1],
                permissions: is[2]
            }
        })

        if (scope === "offwebLogin") { return policies.join("#") } // 官网登入，存入账户可使用的权限

        const spa = scope.split("|")
        const contains = plc.find((item) =>
            spa[0] === item.client && (item.resource.indexOf(spa[1]) !== -1 || item.resource === "*"))
        sp = [contains.client, contains.resource , contains.permissions].join("|")
        return sp
    }
}
