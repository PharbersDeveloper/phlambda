
import { AuthorizationCode, Client, Token, User } from "../interfaces"
import { AuthorizationCodeModel } from "../interfaces/model.interface"
import { Request } from "../request"

export class Pharbers implements AuthorizationCodeModel {
    // -------------------BaseModel----------------------
    public request: Request

    public async getClient(
        clientId: string,
        clientSecret?: string): Promise<Client> {

            console.info(clientId)
            console.info(clientSecret)
            throw new Error("Not Implemented Model getClient")
    }

    public generateAccessToken(
        client: Client,
        user: User,
        scope: string): Promise<string> {

            console.info(client)
            console.info(user)
            console.info(scope)
            throw new Error("Not Implemented Model generateAccessToken")
     }

    public async saveToken(token: Token, client: Client, user: User): Promise<Token> {

        console.info(token)
        console.info(client)
        console.info(user)
        throw new Error("Not Implemented Model saveToken")
    }

    // --------------------RequestAuthenticationModel----------------------
    public async getAccessToken(accessToken: string): Promise<Token> {
        console.info(accessToken)
        throw new Error("Not Implemented Model getAccessToken")
    }

    public async verifyScope(token: Token, scope: string): Promise<boolean> {
        console.info(token)
        console.info(scope)
        throw new Error("Not Implemented Model verifyScope")
    }

    // ---------------------AuthorizationCodeModel---------------------
    public async generateRefreshToken(client: Client, user: User, scope: string): Promise<string> {
        console.info(client)
        console.info(user)
        console.info(scope)
        throw new Error("Not Implemented Model generateRefreshToken")
    }

    public async generateAuthorizationCode(client: Client, user: User, scope: string): Promise<string> {
        console.info(client)
        console.info(user)
        console.info(scope)
        throw new Error("Not Implemented Model generateAuthorizationCode")
    }

    public async getAuthorizationCode(authorizationCode: string): Promise<AuthorizationCode> {
        console.info(authorizationCode)
        throw new Error("Not Implemented Model getAuthorizationCode")
    }

    public async saveAuthorizationCode(
        code: AuthorizationCode,
        client: Client,
        user: User): Promise<AuthorizationCode> {
            console.info(code)
            console.info(client)
            console.info(user)
            throw new Error("Not Implemented Model saveAuthorizationCode")
    }

    public async revokeAuthorizationCode(code: AuthorizationCode): Promise<boolean> {
        console.info(code)
        throw new Error("Not Implemented Model revokeAuthorizationCode")
    }

    public async validateScope(
        user: User,
        client: Client,
        scope: string): Promise<string> {

            console.info(user)
            console.info(client)
            console.info(scope)
            throw new Error("Not Implemented Model validateScope")
    }

}
