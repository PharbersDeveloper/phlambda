
import { Logger, SF, Store } from "phnodelayer"
import { AuthorizationCode, Client, Token, User } from "../interfaces"
import { AuthorizationCodeModel } from "../interfaces/model.interface"
import { Request } from "../request"

export class Pharbers implements AuthorizationCodeModel {
    // -------------------BaseModel----------------------
    request: Request

    async getClient(clientId: string, clientSecret?: string | undefined): Promise<Client> {
            Logger.info(clientId)
            Logger.info(clientSecret)
            const pg = SF.getInstance.get(Store.Postgres)
            const result = await pg.find("client", [clientId], {})
            if (result.payload.records.length === 0) {
                return null
            }
            const record = result.payload.records[0]
            if (record.expired !== null && record.expired > new Date()) {
                return null
            }

            return {
                id: clientId,
                redirectUris: record.registerRedirectUri,
                grants: ["authorizationCode", "authorization_code"],
                accessTokenLifetime: 60 * 60, // 1 小时
                refreshTokenLifetime: 60 * 60,
                secret: record.secret
            }
    }

    generateAccessToken(client: Client, user: User, scope: string): Promise<string> {

            Logger.info(client)
            Logger.info(user)
            Logger.info(scope)
            throw new Error("Not Implemented Model generateAccessToken")
     }

    async saveToken(token: Token, client: Client, user: User): Promise<Token> {

        Logger.info(token)
        Logger.info(client)
        Logger.info(user)
        throw new Error("Not Implemented Model saveToken")
    }

    // --------------------RequestAuthenticationModel----------------------
    async getAccessToken(accessToken: string): Promise<Token> {
        Logger.info(accessToken)
        throw new Error("Not Implemented Model getAccessToken")
    }

    async verifyScope(token: Token, scope: string): Promise<boolean> {
        Logger.info(token)
        Logger.info(scope)
        throw new Error("Not Implemented Model verifyScope")
    }

    // ---------------------AuthorizationCodeModel---------------------
    async generateRefreshToken(client: Client, user: User, scope: string): Promise<string> {
        Logger.info(client)
        Logger.info(user)
        Logger.info(scope)
        throw new Error("Not Implemented Model generateRefreshToken")
    }

    async generateAuthorizationCode(client: Client, user: User, scope: string): Promise<string> {
        Logger.info(client)
        Logger.info(user)
        Logger.info(scope)
        throw new Error("Not Implemented Model generateAuthorizationCode")
    }

    async getAuthorizationCode(authorizationCode: string): Promise<AuthorizationCode> {
        Logger.info(authorizationCode)
        throw new Error("Not Implemented Model getAuthorizationCode")
    }

    async saveAuthorizationCode(code: AuthorizationCode, client: Client, user: User): Promise<AuthorizationCode> {
            Logger.info(code)
            Logger.info(client)
            Logger.info(user)
            throw new Error("Not Implemented Model saveAuthorizationCode")
    }

    async revokeAuthorizationCode(code: AuthorizationCode): Promise<boolean> {
        Logger.info(code)
        throw new Error("Not Implemented Model revokeAuthorizationCode")
    }

    async validateScope(user: User, client: Client, scope: string): Promise<string> {

            Logger.info(user)
            Logger.info(client)
            Logger.info(scope)
            throw new Error("Not Implemented Model validateScope")
    }

}
