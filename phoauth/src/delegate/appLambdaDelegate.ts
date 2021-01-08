import CryptoJS from "crypto-js"
import { ServerResponse } from "http"
import moment from "moment"
import { AWSRequest, ConfigRegistered, Logger, PostgresConfig, RedisConfig, SF, Store } from "phnodelayer"
import {
    errors2response,
    PhInvalidAuthGrant,
    PhInvalidAuthorizationLogin,
    PhInvalidClient,
    PhInvalidGrantType,
    PhInvalidParameters,
    PhInvalidPassword,
    PhNotFoundError,
    PhRecordLoss
} from "../errors/pherrors"

export default class AppLambdaDelegate {
    public rds: any = null
    public pg: any = null
    public async exec(event: Map<string, any>) {
        const pg = new PostgresConfig("oauth", "pharbers", "Abcde196125", "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn", 5432, "phcommon")
        const redis = new RedisConfig("token", "", "", "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn", 6379, "0")
        ConfigRegistered.getInstance.registered(pg).registered(redis)
        this.rds = SF.getInstance.get(Store.Redis)
        this.pg = SF.getInstance.get(Store.Postgres)
        await this.pg.open()
        await this.rds.open()
        try {
            // @ts-ignore
            if (!event.body) {
                // @ts-ignore
                event.body = ""
            }
            const req = new AWSRequest(event, "oauth")
            const response = new ServerResponse(req)
            // @ts-ignore
            const endpoint = event.pathParameters.edp
            if (endpoint === "login") {
                await this.loginHandler(event, response)
            } else if (endpoint === "authorization") {
                await this.authHandler(event, response)
            } else if (endpoint === "token") {
                await this.tokenHandler(event, response)
            }
            return response
        } catch (e) {
            throw e
        } finally {
            await this.pg.close()
            await this.rds.close()
        }
    }
    // 兼容产品的登入注册前端页面走向逻辑
    protected async loginHandler(event: Map<string, any>, response: ServerResponse) {
        // @ts-ignore
        const email = event.queryStringParameters.email
        // @ts-ignore
        const result = await this.pg.find("account", null, { match: { email } })
        if (result.payload.records.length === 0) {
            errors2response(PhNotFoundError, response)
            return response
        }
        const records = result.payload.records
        if (records.length === 1 && (records.password !== "" || records.password !== null)) {
            const account = records[0]
            // @ts-ignore
            if (account.password === event.queryStringParameters.password) {
                // @ts-ignore
                response.statusCode = 200
                // @ts-ignore
                response.headers = { "Content-Type": "application/json", "Accept": "application/json" }
                // @ts-ignore
                response.body = { message: "login success", uid: account.id }
            } else {
                errors2response(PhInvalidPassword, response)
            }
        } else {
            errors2response(PhRecordLoss, response)
        }

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
        const flag  = event.queryStringParameters.user_id // 定位user id
        if (!flag) {
            errors2response(PhInvalidAuthorizationLogin, response)
            return response
        }
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
        const client = await this.pg.find("client", clientId)
        const clientRecord = client.payload.records[0]
        if (client.payload.records.length === 0) {
            errors2response(PhInvalidClient, response)
            return response
        }
        if (clientRecord.expired !== null && clientRecord.expired < new Date()) {
            errors2response(PhInvalidClient, response)
            return response
        }
        const clientName = clientRecord.name

        // @ts-ignore
        let scope = event.queryStringParameters.scope // 不同前端项目对应不同的client和scope
        if (scope === undefined) {
            scope = ["APP", `${clientName}:*:*:R`, "R"].join("|")
        }

        // @ts-ignore
        const userId = event.queryStringParameters.user_id
        const account = await this.pg.find("account", userId, null, ["defaultRole", "scope"])
        if (account.payload.records.length === 0) {
            errors2response(PhNotFoundError, response)
            return response
        }
        const employerId = account.payload.records[0].employer
        const scopeRecord = account.payload.include.scope.map((x) =>
            x.name.toLowerCase() === "default" ?
                {name: x.name, value: x.scopePolicy.replace("{uid}", userId).replace("{pid}", employerId)} :
                {name: x.name, value: x.scopePolicy}
        )
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
            response.body =
                "code=" +
                (await this.genAuthCode(userId, clientId, scope)) +
                "&redirect_uri=" +
                redirectUri +
                "&state=" +
                state
        } else {
            // @ts-ignore
            response.body = "code=" + (await this.genAuthCode(userId, clientId, scope)) + "&state=" + state
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

        const client = await this.pg.find("client", clientId)
        if (client.payload.records.length === 0) {
            errors2response(PhNotFoundError, response)
            return response
        }

        if (grantType !== "authorization_code") {
            errors2response(PhInvalidGrantType, response)
            return response
        }

        const codeRecord = await this.rds.find("authorization", null, { match: { code } })
        if (codeRecord.payload.records.length === 0) {
            errors2response(PhInvalidParameters, response)
            return response
        }
        const content = codeRecord.payload.records[0]

        // TODO: Check register redirect URI
        // if (content.redirectUri !== redirectUri ||
        //     content.clientId !== clientId) {
        //     errors2response(PhInvalidParameters, response)
        //     return response
        // }

        const accessToken = await this.genAccessToken(content.uid, clientId, content.scope)

        // @ts-ignore
        const result = await this.pg.find("account", accessToken.uid )
        if (result.payload.records.length === 0) {
            errors2response(PhNotFoundError, response)
            return response
        }
        const record = result.payload.records[0]

        // @ts-ignore
        response.statusCode = 200
        // @ts-ignore
        response.headers = { "Content-Type": "application/json" }
        // @ts-ignore
        response.body = {
            username: record.name,
            first_name: record.firstName,
            last_name: record.lastName,
            email: record.email,
            access_token: accessToken.token,
            token_type: "bearer",
            expires_in: 64800,
            refresh_token: accessToken.refresh,
            uid: accessToken.uid,
        }
        return response
    }

    protected grantScopeAuth(scope: string, policies: any[]) {
        if (policies.length === 0) { // 无任何权限
            return false
        }
        // @ts-ignore
        if (policies.length === 1 && policies[0].value === "*") { // 权限为admin
            return true
        }
        if (scope.toLowerCase().includes("sso")) { // 官网登入，直接放行，交由后续的mapping policies设置该账户可使用权限
            return true
        }
        const sa = scope.split("|")

        // 拥有指定资源或所有资源
        const contains = this.getAccessScope(scope, policies)
        if (contains === undefined) { // 申请的资源不再数据库中
            return false
        }
        if (contains.permissions === "A") { // 权限为A，scope权限申请，放行
            return true
        }
        if (sa[2] === "R" && contains.permissions !== "R") { // 权限为W|X，scope申请为R，放行
            return true
        } else { // 权限为W|X，申请权限必须与预期相等
            return contains.permissions === sa[2]
        }
    }

    protected async genAuthCode(uid: string, cid: string, scope: string) {
        const time = 2
        const now = new Date()
        const exp = moment(now).add(time, "m").toDate()
        const code = this.hexEncode(this.hash(uid + cid + new Date().toISOString() + Math.random().toString()))
        const authCode = { uid, cid, code, scope, create: now, expired: exp }
        const result = await this.rds.create("authorization", authCode)
        const seconds = (authCode.expired.getTime() - authCode.create.getTime()) / 1000
        // tslint:disable-next-line:max-line-length
        await this.rds.setExpire(
            `authorization:${result.payload.records[0].id}`,
            JSON.stringify(result.payload.records[0]),
            seconds.toFixed(0),
        )
        return code
    }

    protected async genAccessToken(uid: string, cid: string, scope: string) {
        const time = 1
        const now = new Date()
        const exp = moment(now).add(time, "week").toDate()
        const accessToken = this.hexEncode(this.hash(cid + now.toISOString() + Math.random().toString()))
        // const refreshToken = this.hexEncode(this.hash(cid + new Date().toISOString() + Math.random().toString()))
        const tk = { uid, cid, token: accessToken, refresh: accessToken, create: now, expired: exp, scope }
        const result = await this.rds.create("access", tk)
        const seconds = (tk.expired.getTime() - tk.create.getTime()) / 1000
        // tslint:disable-next-line:max-line-length
        await this.rds.setExpire(
            `access:${result.payload.records[0].id}`,
            JSON.stringify(result.payload.records[0]),
            seconds.toFixed(0),
        )
        return tk
    }

    protected hexEncode(value) {
        return value.toString(CryptoJS.enc.Hex)
    }

    // protected hmac(secret, value) {
    //     return CryptoJS.HmacSHA256(value, secret, { asBytes: true })
    // }

    protected hash(value) {
        return CryptoJS.SHA256(value)
    }

    protected mappingPolices(scope: string, policies: any[]) {
        // @ts-ignore
        if (policies.length === 1 && policies[0].value === "*") { // 权限为admin
            return "*"
        }
        if (scope.toLowerCase().includes("sso")) { // 官网登入，存入账户可使用的权限
            // @ts-ignore
            return policies.map((item: any) => item.value).join("#")
        }

        // TODO: 现在一个系统会调用另一个系统不能给最小权限不然后续验证时不会放行其他请求，这个还需要重新思考，暂时给数据库绑定的权限
        // let sp
        // const contains = this.getAccessScope(scope, policies)
        // sp = [
        //     [contains.client, contains.resource, contains.permissions].join("|"),
        //     policies.find((item: any) => item.name.toLowerCase() === "default").value
        // ].filter((item: string) => item !== undefined).join("#")
        // return sp
        return policies.map((item: any) => item.value).join("#")
    }

    /**
     * 获取用户申请访问权限区间
     * @param scope
     * @param policies
     */
    private getAccessScope(scope: string, policies: any[]): any {
        const plc = policies.map((item: any) => {
            // @ts-ignore
            const is = item.value.split("|")
            return {
                client: is[0],
                resource: is[1],
                permissions: is[2],
            }
        })
        // TODO: 后续暴露API接入三方，这边的查找范围是有问题的，应从匹配单个 => 匹配多个Scope，先满足现有后续再改吧
        const sa = scope.split("|")
        return plc.find((item) => {
            const resourceTypes = Array.from(new Set(item.resource.split(",").map((resource) => {
                return resource.split(":")[0]
            })))
            return sa[0] === item.client && (resourceTypes.includes(sa[1].split(":")[0]) || item.resource === "*")
        })
    }
}
