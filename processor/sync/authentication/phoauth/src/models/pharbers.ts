
import { IStore, Logger, Register, StoreEnum } from "phnodelayer"
import Crypto from "../common/crypto"
import {AuthorizationCode, Client, RefreshToken, Token, User} from "../interfaces"
import { AuthorizationCodeModel, Model } from "../interfaces/model.interface"
import { Request } from "../request"

export class Pharbers implements Model {
    // -------------------BaseModel----------------------
    request: Request

    async getClient(clientId: string, clientSecret?: string | undefined): Promise<Client> {
        // const pg = SF.getInstance.get(Store.Postgres)
        const pg = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
        const result = await pg.find("client", [clientId], {})
        if (result.payload.records.length === 0) {
            return null
        }
        const record = result.payload.records[0]
        if (record.expired !== null && record.expired < new Date()) {
            return null
        }

        return {
            id: clientId,
            name: record.name,
            redirectUris: record.registerRedirectUri,
            grants: ["authorizationCode", "authorization_code", "refreshToken",
                "refresh_token", "implicit", "password"],
            secret: record.secret
        }
    }

    generateAccessToken(client: Client, user: User, scope: string): Promise<string> {
        const cc = new Crypto()
        return cc.hexEncode(cc.hash(client.id + user.id + scope + new Date().toISOString() + Math.random().toString()))
     }

    async saveToken(token: Token, client: Client, user: User): Promise<Token> {
        // const redis = SF.getInstance.get(Store.Redis)
        const redis = Register.getInstance.getData(StoreEnum.REDIS) as IStore
        const tk = {
            uid: user.id, cid: client.id,
            token: token.accessToken, refresh: token.refreshToken,
            expired: token.accessTokenExpiresAt, scope: token.scope, refreshExpired: token.refreshTokenExpiresAt }
        const result = await redis.create("access", tk)
        const seconds = (tk.refreshExpired.getTime() - new Date().getTime()) / 1000
        const store = redis.getStore()
        store.adapter.redis.set(
            `access:${result.payload.records[0].id}`,
            JSON.stringify(result.payload.records[0]),
            "EX",
            seconds.toFixed(0),
        )
        token.client = client
        token.user = user
        // delete token.scope
        // delete token.user.scope
        return token
    }

    // --------------------RequestAuthenticationModel----------------------
    async getAccessToken(accessToken: string): Promise<Token> {
        // const redis = SF.getInstance.get(Store.Redis)
        const redis = Register.getInstance.getData(StoreEnum.REDIS) as IStore
        const result = await redis.find("access", null, { match: { token: accessToken } })
        if (result.payload.records.length === 0) {
            return null
        }
        const record = result.payload.records[0]
        return {
            accessToken: record.token,
            accessTokenExpiresAt: record.expired,
            refreshToken: record.refresh,
            refreshTokenExpiresAt: record.refreshExpired,
            scope: record.scope,
            client: await this.getClient(record.cid),
            user: await this.getUserById(record.uid)
        }
    }

    async verifyScope(token: Token, scope: string): Promise<boolean> {
        Logger.info(token)
        Logger.info(scope)
        throw new Error("Not Implemented Model verifyScope")
    }

    // ---------------------AuthorizationCodeModel---------------------
    async generateRefreshToken(client: Client, user: User, scope: string): Promise<string> {
        const cc = new Crypto()
        return cc.hexEncode(cc.hash(client.id + user.id + scope + new Date().toISOString() + Math.random().toString()))
    }

    async generateAuthorizationCode(client: Client, user: User, scope: string): Promise<string> {
        const cc = new Crypto()
        return cc.hexEncode(cc.hash(user.id + client.id + new Date().toISOString() + Math.random().toString()))
    }

    async getAuthorizationCode(authorizationCode: string): Promise<AuthorizationCode> {
        // const redis = SF.getInstance.get(Store.Redis)
        const redis = Register.getInstance.getData(StoreEnum.REDIS) as IStore
        const result = await redis.find("authorization", null, { match: { code: authorizationCode } })
        if (result.payload.records.length === 0) {
            return null
        }
        const record = result.payload.records[0]
        return {
            authorizationCode: record.code,
            expiresAt: record.expired,
            redirectUri: record.redirectUri,
            scope: record.scope,
            client: await this.getClient(record.cid),
            user: await this.getUserById(record.uid)
        }
    }

    async saveAuthorizationCode(code: AuthorizationCode, client: Client, user: User): Promise<AuthorizationCode> {
        // const redis = SF.getInstance.get(Store.Redis)
        const redis = Register.getInstance.getData(StoreEnum.REDIS) as IStore
        const authCode = { uid: user.id, cid: client.id,
            code: code.authorizationCode, redirectUri: code.redirectUri,
            scope: code.scope, expired: code.expiresAt }
        const seconds = (authCode.expired.getTime() - new Date().getTime()) / 1000
        const result = await redis.create("authorization", authCode)
        const store = redis.getStore()
        store.adapter.redis.set(
            `authorization:${result.payload.records[0].id}`,
            JSON.stringify(result.payload.records[0]),
            "EX",
            seconds.toFixed(0),
        )
        return code
    }

    async revokeAuthorizationCode(code: AuthorizationCode): Promise<boolean> {
        // const redis = SF.getInstance.get(Store.Redis)
        const redis = Register.getInstance.getData(StoreEnum.REDIS) as IStore
        let result = await redis.find("authorization", null, { match: { code: code.authorizationCode } })
        if (result.payload.records.length === 0) {
            return false
        }
        const record = result.payload.records[0]
        result = await redis.delete("authorization", record.id)
        return result.payload.records.length !== 0
    }

    async validateScope(user: User, client: Client, scope: string): Promise<string> {
            let cpScope = scope

            if (scope === undefined) {
                cpScope = ["APP", `${client.name}:*:*:R`, "R"].join("|")
            }

            const flag = cpScope.indexOf("#") > -1 ?
                cpScope.split("#").map((x: string) => this.grantScopeAuth(x, user.scope)).includes(true) :
                this.grantScopeAuth(cpScope, user.scope)

            if (!user || !client || !flag) {
                return null
            }
            if (user.scope.length === 1 && user.scope[0].value === "*") { // ?????????admin
                return "*"
            }
            if (cpScope.toLowerCase().includes("sso")) { // ?????????????????????????????????????????????
                return user.scope.map((item: any) => item.value).join("#")
            }

            // TODO: ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
            // let sp
            // const contains = this.getAccessScope(cpScope, user.scope)
            // sp = [
            //     [contains.client, contains.resource, contains.permissions].join("|"),
            //     policies.find((item: any) => item.name.toLowerCase() === "default").value
            // ].filter((item: string) => item !== undefined).join("#")
            // return sp
            return user.scope.map((item: any) => item.value).join("#")
    }

    async getUserById(userId: string): Promise<User> {
        const pg = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
        const result = await pg.find("account", userId, null, ["defaultRole", "scope"])
        if (result.payload.count === 0) {
            return null
        }
        const record = result.payload.records[0]
        record.include = result.payload.include || {}
        return {
            id: record.id,
            name: record.name,
            firstName: record.firstName,
            lastName: record.lastName,
            employerId: record.employer,
            email: record.email,
            scope: record.include.scope.map((x) =>
                x.name.toLowerCase() === "default" ?
                    {name: x.name, value: x.scopePolicy.replace("{uid}", userId).replace("{pid}", record.employer)} :
                    {name: x.name, value: x.scopePolicy}
            )
        }
    }

    async getUser(username: string, password: string, thirdpartyType?: string,
                  thirdpartyToken?: string, additionalOptions?: any): Promise<User> {
        const pg = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore

        const result = await pg.find("account",
            null,
            { match: { email: decodeURIComponent(username), password}},
            ["defaultRole", "scope"])

        if (result.payload.count === 0) {
            return null
        }
        return this.getUserById(result.payload.records[0].id)
    }
    // ---------------------RefreshTokenModel---------------------
    async getRefreshToken(refreshToken: string): Promise<RefreshToken> {
        // const redis = SF.getInstance.get(Store.Redis)
        const redis = Register.getInstance.getData(StoreEnum.REDIS) as IStore
        const result = await redis.find("access", null, { match: { refresh: refreshToken } })
        if (result.payload.records.length === 0) {
            return null
        }
        const record = result.payload.records[0]
        return {
            refreshToken: record.refresh,
            refreshTokenExpiresAt: record.refreshExpired,
            scope: record.scope,
            client: await this.getClient(record.cid),
            user: await this.getUserById(record.uid)
        }
    }

    async revokeToken(token: RefreshToken | Token): Promise<boolean> {
        // const redis = SF.getInstance.get(Store.Redis)
        const redis = Register.getInstance.getData(StoreEnum.REDIS) as IStore
        let result
        if (token.hasOwnProperty("accessToken")) {
            result = await redis.find("access", null, { match: { token: token.accessToken } })
        } else {
            result = await redis.find("access", null, { match: { refresh: token.refreshToken } })
        }

        if (result.payload.records.length === 0) {
            return false
        }
        const record = result.payload.records[0]
        result = await redis.delete("access", record.id)
        return result.payload.records.length !== 0
    }

    //
    async getUserFromClient(client: Client): Promise<User> {
        throw new Error("getUserFromClient is not Impl")
    }

    /**
     * ????????????Scope????????????
     * @param scope
     * @param policies
     */
    private grantScopeAuth(scope: string, policies: any[]) {
        if (policies.length === 0) { // ???????????????
            return false
        }
        // @ts-ignore
        if (policies.length === 1 && policies[0].value === "*") { // ?????????admin
            return true
        }
        if (scope.toLowerCase().includes("sso")) { // ?????????????????????????????????????????????mapping policies??????????????????????????????
            return true
        }
        const sa = scope.split("|")

        // ?????????????????????????????????
        const contains = this.getAccessScope(scope, policies)
        if (contains === undefined) { // ?????????????????????????????????
            return false
        }
        if (contains.permissions === "A") { // ?????????A???scope?????????????????????
            return true
        }
        if (sa[2] === "R" && contains.permissions !== "R") { // ?????????W|X???scope?????????R?????????
            return true
        } else { // ?????????W|X????????????????????????????????????
            return contains.permissions === sa[2]
        }
    }

    /**
     * ????????????????????????????????????
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
        // TODO: ????????????API???????????????????????????????????????????????????????????????????????? => ????????????Scope?????????????????????????????????
        const sa = scope.split("|")
        return plc.find((item) => {
            const resourceTypes = Array.from(new Set(item.resource.split(",").map((resource) => {
                return resource.split(":")[0]
            })))
            return sa[0] === item.client && (resourceTypes.includes(sa[1].split(":")[0]) || item.resource === "*")
        })
    }

}
