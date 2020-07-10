import {ServerResponse} from "http"
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
const CryptoJS = require("crypto-js");
import moment from "moment"

/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */
export default class AppLambdaAuthDelegate extends AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
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
        }
        return response
    }

    protected async loginHandler(event: Map<string, any>, response: ServerResponse) {
        // @ts-ignore
        const body = JSON.parse(event.body)
        const email = body.email
        // @ts-ignore
        const result = await this.store.find("account", null, { match: { email } } )
        // const response = {}
        if (result.payload.records.length === 0) {
            // @ts-ignore
            response.statusCode = 404
            // @ts-ignore
            response.headers = { "Content-Type": "application/json", "Accept": "application/json" }
            // @ts-ignore
            response.body = "User Not Found"
        } else if (result.payload.records.length === 1) {

            const account = result.payload.records[0]
            phLogger.info(account)

            if (account.password === body.password) {
                // @ts-ignore
                response.statusCode = 200
                // @ts-ignore
                response.headers = { "Content-Type": "application/json", "Accept": "application/json" }
                // @ts-ignore
                response.body = result.payload.records[0]
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
        const redirectUri = event.queryStringParameters.redirect_uri
            // @ts-ignore
        const responseType = event.queryStringParameters.response_type
        if (responseType !== "code") {
            errors2response(PhInvalidParameters, response)
            return response
        }
        // @ts-ignore
        const clientId = event.queryStringParameters.client_id
        // @ts-ignore
        const client = await this.store.find("client", clientId)
        const clientRecord = client.payload.records[0]
        if (clientRecord.expired !== null && clientRecord.expired < new Date()) {
            errors2response(PhInvalidClient, response)
            return response
        }
        const clientName = clientRecord.name

        // @ts-ignore
        let scope = event.queryStringParameters.scope
        if (scope === undefined) {
            scope = ["APP", clientName, "R"].join("|")
        }

        // @ts-ignore
        const userId = event.queryStringParameters.user_id
        const account = await this.store.find("account", userId, null, ["defaultRole", "scope"])
        const scopeRecord = account.payload.include.scope[0].map (x => x.scopePolicy)
        if (!this.grantScopeAuth(scope, scopeRecord)) {
            errors2response(PhInvalidAuthGrant, response)
            return response
        }

        // @ts-ignore
        let state = event.queryStringParameters.state
        if (state === null) {
            state = "xyz"
        }

        if (redirectUri !== null) {
            // @ts-ignore
            response.statusCode = 302
            // @ts-ignore
            response.headers = {
                Location: redirectUri + "?code=" + await this.genAuthCode(userId, clientId, scope) + "&state=" + state,
                "Content-Type": "application/x-www-form-urlencoded"
            }
        } else {
            // @ts-ignore
            response.statusCode = 200
            // @ts-ignore
            response.body = "code=" + await this.genAuthCode(userId, clientId, scope) + "&state=" + state
            // @ts-ignore
            response.headers = { "Content-Type": "application/x-www-form-urlencoded" }
        }


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
        phLogger.info(content)

        if (content.redirectUri !== redirectUri ||
            content.clientId !== clientId) {

            errors2response(PhInvalidParameters, response)
            return response
        }

        const accessToken = await this.genAccessToken(clientId)

        // @ts-ignore
        response.statusCode = 200
        // @ts-ignore
        response.headers = { "Content-Type": "application/x-www-form-urlencoded" }
        // @ts-ignore
        response.body = {
            "access_token": accessToken.token,
            "token_type": "bearer",
            "expires_in": 64800,
            "refresh_token": accessToken.refresh,
        }
        return response
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
        const exp = moment(new Date()).add(10, 'm').toDate()
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

    protected hexEncode(value) {
        return value.toString(CryptoJS.enc.Hex);
    }

    protected hmac(secret, value) {
        return CryptoJS.HmacSHA256(value, secret, {asBytes: true});
    }

    protected hash(value) {
        return CryptoJS.SHA256(value);
    }
}