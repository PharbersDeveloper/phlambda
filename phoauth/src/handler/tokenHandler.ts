import { ServerResponse } from "http"
import moment from "moment"
import Crypto from "../common/crypto"
import {
    errors2response, PhInvalidGrantType,
    PhInvalidParameters, PhNotFoundError,
} from "../errors/pherrors"
import { IHandler } from "./IHandler"

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
export default class TokenHandler implements IHandler {
    public async execute(event: any, response: ServerResponse, pg: any, redis: any) {
        const redirectUri = event.queryStringParameters.redirect_uri
        const clientId = event.queryStringParameters.client_id
        const code = event.queryStringParameters.code
        const grantType = event.queryStringParameters.grant_type

        const client = await pg.find("client", clientId)
        if (client.payload.records.length === 0) {
            errors2response(PhNotFoundError, response)
            return response
        }

        if (grantType !== "authorization_code") {
            errors2response(PhInvalidGrantType, response)
            return response
        }

        const codeRecord = await redis.find("authorization", null, { match: { code } })
        if (codeRecord.payload.records.length === 0) {
            errors2response(PhInvalidParameters, response)
            return response
        }
        const content = codeRecord.payload.records[0]

        if (content.registerRedirectUri[0] !== redirectUri ||
            content.clientId !== clientId) {
            errors2response(PhInvalidParameters, response)
            return response
        }

        const accessToken = await this.genAccessToken(content.uid, clientId, content.scope, redis)

        // @ts-ignore
        const result = await pg.find("account", accessToken.uid )
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

    private async genAccessToken(uid: string, cid: string, scope: string, redis: any) {
        const time = 1
        const now = new Date()
        const exp = moment(now).add(time, "week").toDate()
        const cc = new Crypto()
        const accessToken = cc.hexEncode(cc.hash(cid + now.toISOString() + Math.random().toString()))
        // const refreshToken = this.hexEncode(this.hash(cid + new Date().toISOString() + Math.random().toString()))
        const tk = { uid, cid, token: accessToken, refresh: accessToken, create: now, expired: exp, scope }
        const result = await redis.create("access", tk)
        const seconds = (tk.expired.getTime() - tk.create.getTime()) / 1000
        // tslint:disable-next-line:max-line-length
        await redis.setExpire(
            `access:${result.payload.records[0].id}`,
            JSON.stringify(result.payload.records[0]),
            seconds.toFixed(0),
        )
        return tk
    }

}
