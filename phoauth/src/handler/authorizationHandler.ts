import { ServerResponse } from "http"
import moment from "moment"
import Crypto from "../common/crypto"
import {
    errors2response, PhInvalidAuthGrant,
    PhInvalidAuthorizationLogin, PhInvalidClient, PhInvalidParameters,
    PhNotFoundError
} from "../errors/pherrors"
import { IHandler } from "./IHandler"

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
export default class AuthorizationHandler implements IHandler {
    public async execute(event: any, response: ServerResponse, pg: any, redis: any) {
        const redirectUri = event.queryStringParameters.redirect_uri // 重定向
        const responseType = event.queryStringParameters.response_type // code?
        if (responseType !== "code") {
            errors2response(PhInvalidParameters, response)
            return response
        }
        const clientId = event.queryStringParameters.client_id // client 是干啥的
        const client = await pg.find("client", clientId)
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

        let scope = event.queryStringParameters.scope // 不同前端项目对应不同的client和scope
        if (scope === undefined) {
            scope = ["APP", `${clientName}:*:*:R`, "R"].join("|")
        }

        const userId = event.queryStringParameters.user_id // 暂时定位user id，没有的统一认为是接入OAuth
        if (!userId) {
            // TODO: 不是正确解法，正确应该将AWS APIGetaway的鉴权去掉（None）
            // TODO Authorization、Token的跳转不应该交由前端去完成，后端应该直接返回302 location定位到匹配url
            // TODO 为了优先稳定只能在这边做了不正确的解法
            // @ts-ignore
            PhInvalidAuthorizationLogin.headers.location =
                `http://accounts.pharbers.com/welcome?redirect_uri=${clientRecord.domain[0]}`
            errors2response(PhInvalidAuthorizationLogin, response)
            return response
        }

        const account = await pg.find("account", userId, null, ["defaultRole", "scope"])
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

        let state = event.queryStringParameters.state
        if (state === null || state === undefined) {
            state = "xyz"
        }

        // TODO 应该直接返回302状态 location定位到使用者的callback，callback、domain地址存到数据库中，符合大厂规范

        response.statusCode = 200
        if (clientId !== "XwgxtaFThqfJ4lru-a-") {
            // TODO 目前自家产品都是使用本clientid进行登入因此跳过第三方介入，但这里如上面描述一样不是正解
            // @ts-ignore
            response.body =
                "code=" +
                (await this.genAuthCode(userId, clientId, scope, redis)) +
                "&redirect_uri=" +
                clientRecord.registerRedirectUri[0] +
                "&state=" +
                state
        } else if (redirectUri) {
            // @ts-ignore
            response.body =
                "code=" +
                (await this.genAuthCode(userId, clientId, scope, redis)) +
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

    private mappingPolices(scope: string, policies: any[]) {
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

    private grantScopeAuth(scope: string, policies: any[]) {
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

    private async genAuthCode(uid: string, cid: string, scope: string, redis: any) {
        const time = 2
        const now = new Date()
        const exp = moment(now).add(time, "m").toDate()
        const cc = new Crypto()
        const code = cc.hexEncode(cc.hash(uid + cid + new Date().toISOString() + Math.random().toString()))
        const authCode = { uid, cid, code, scope, create: now, expired: exp }
        const result = await redis.create("authorization", authCode)
        const seconds = (authCode.expired.getTime() - authCode.create.getTime()) / 1000
        await redis.setExpire(
            `authorization:${result.payload.records[0].id}`,
            JSON.stringify(result.payload.records[0]),
            seconds.toFixed(0),
        )
        return code
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
