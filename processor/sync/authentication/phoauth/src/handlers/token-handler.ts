import auth from "basic-auth"
import {
    InvalidArgumentError,
    InvalidClientError,
    InvalidRequestError,
    OAuthError,
    ServerError,
    UnauthorizedClientError,
    UnsupportedGrantTypeError,
} from "../errors"
import {
    AuthorizationCodeGrantType,
    ClientCredentialsGrantType,
    PasswordGrantType,
    RefreshTokenGrantType,
} from "../grant-types"
import { Client, Model } from "../interfaces"
import { TokenModel } from "../models"
import { Request } from "../request"
import { Response } from "../response"
import { BearerTokenType } from "../token-types"
import { hasOwnProperty } from "../utils/fn"
import * as is from "../validator/is"

/**
 * Grant types.
 */

const grantTypes = {
    authorizationCode: AuthorizationCodeGrantType,
    clientCredentials: ClientCredentialsGrantType,
    password: PasswordGrantType,
    refreshToken: RefreshTokenGrantType,
}
export class TokenHandler {
    accessTokenLifetime: any
    grantTypes: { [key: string]: any }
    model: Model
    refreshTokenLifetime: number
    allowExtendedTokenAttributes: boolean
    requireClientAuthentication: any
    alwaysIssueNewRefreshToken: boolean
    constructor(options: any = {}) {
        if (!options.accessTokenLifetime) {
            throw new InvalidArgumentError(
                "Missing parameter: `accessTokenLifetime`",
            )
        }

        if (!options.model) {
            throw new InvalidArgumentError("Missing parameter: `model`")
        }

        if (!options.refreshTokenLifetime) {
            throw new InvalidArgumentError(
                "Missing parameter: `refreshTokenLifetime`",
            )
        }

        if (!options.model.getClient) {
            throw new InvalidArgumentError(
                "Invalid argument: model does not implement `getClient()`",
            )
        }

        this.accessTokenLifetime = options.accessTokenLifetime
        this.grantTypes = { ...grantTypes, ...options.extendedGrantTypes }
        this.model = options.model
        this.refreshTokenLifetime = options.refreshTokenLifetime
        this.allowExtendedTokenAttributes = options.allowExtendedTokenAttributes
        this.requireClientAuthentication =
            options.requireClientAuthentication || {}
        this.alwaysIssueNewRefreshToken =
            options.alwaysIssueNewRefreshToken !== false
    }

    /**
     * Token Handler.
     */

    async handle(request: Request, response: Response) {
        if (!(request instanceof Request)) {
            throw new InvalidArgumentError(
                "Invalid argument: `request` must be an instance of Request",
            )
        }

        if (!(response instanceof Response)) {
            throw new InvalidArgumentError(
                "Invalid argument: `response` must be an instance of Response",
            )
        }

        if (request.method !== "POST") {
            throw new InvalidRequestError("Invalid request: method must be POST")
        }

        if (!request.is("application/x-www-form-urlencoded")) {
            throw new InvalidRequestError(
                "Invalid request: content must be application/x-www-form-urlencoded",
            )
        }

        // Extend model object with request
        this.model.request = request

        try {
            const client = await this.getClient(request, response)
            const data = await this.handleGrantType(request, client)
            const model = new TokenModel(data, {
                allowExtendedTokenAttributes: this.allowExtendedTokenAttributes,
            })
            const tokenType = this.getTokenType(model)
            this.updateSuccessResponse(response, tokenType)

            return data
        } catch (e) {
            if (!(e instanceof OAuthError)) {
                e = new ServerError(e) // eslint-disable-line no-ex-assign
            }
            this.updateErrorResponse(response, e)
            throw e
        }
    }

    /**
     * Get the client from the model.
     */

    async getClient(request, response) {
        const credentials = this.getClientCredentials(request)
        const grantType = request.body.grantType || request.body.grant_type ||
            request.query.grantType || request.query.grant_type

        if (!credentials.clientId) {
            throw new InvalidRequestError("Missing parameter: `clientId`")
        }

        if (
            this.isClientAuthenticationRequired(grantType) &&
            !credentials.clientSecret
        ) {
            throw new InvalidRequestError("Missing parameter: `clientSecret`")
        }

        if (!is.vschar(credentials.clientId)) {
            throw new InvalidRequestError("Invalid parameter: `clientId`")
        }

        if (credentials.clientSecret && !is.vschar(credentials.clientSecret)) {
            throw new InvalidRequestError("Invalid parameter: `clientSecret`")
        }
        try {
            const client = await this.model.getClient(
                credentials.clientId,
                credentials.clientSecret,
            )
            if (!client) {
                throw new InvalidClientError("Invalid client: client is invalid")
            }

            if (!client.grants) {
                throw new ServerError("Server error: missing client `grants`")
            }

            if (!(client.grants instanceof Array)) {
                throw new ServerError("Server error: `grants` must be an array")
            }

            return client
        } catch (e) {
            // Include the "WWW-Authenticate" response header field if the client
            // attempted to authenticate via the "Authorization" request header.
            //
            // @see https://tools.ietf.org/html/rfc6749#section-5.2.
            if (e instanceof InvalidClientError && request.get("authorization")) {
                response.set("WWW-Authenticate", "Basic realm=\"Service\"")

                throw new InvalidClientError(e, { code: 401 })
            }

            throw e
        }
    }

    /**
     * Get client credentials.
     *
     * The client credentials may be sent using the HTTP Basic authentication scheme or, alternatively,
     * the `clientId` and `clientSecret` can be embedded in the body.
     *
     * @see https://tools.ietf.org/html/rfc6749#section-2.3.1
     */

    getClientCredentials(request: Request) {
        const credentials = auth(request as any)
        const grantType = request.body.grantType || request.body.grant_type ||
            request.query.grant_type || request.query.grant_type

        if (credentials) {
            return {
                clientId: credentials.name,
                clientSecret: credentials.pass,
            }
        }

        if (request.body.clientId && request.body.clientSecret) {
            return {
                clientId: request.body.clientId,
                clientSecret: request.body.clientSecret,
            }
        }

        if (!this.isClientAuthenticationRequired(grantType)) {
            if (request.body.clientId) {
                return { clientId: request.body.clientId }
            }
        }

        throw new InvalidClientError(
            "Invalid client: cannot retrieve client credentials",
        )
    }

    /**
     * Handle grant type.
     */

    async handleGrantType(request: Request, client: Client) {
        let grantType = request.body.grantType || request.body.grant_type ||
            request.query.grantType || request.query.grant_type

        grantType = grantType.replace(/_(\w)/g, (all: any, letter: any) => letter.toUpperCase())

        if (!grantType) {
            throw new InvalidRequestError("Missing parameter: `grantType`")
        }

        if (!is.nchar(grantType) && !is.uri(grantType)) {
            throw new InvalidRequestError("Invalid parameter: `grantType`")
        }

        if (!hasOwnProperty(this.grantTypes, grantType)) {
            throw new UnsupportedGrantTypeError(
                "Unsupported grant type: `grantType` is invalid",
            )
        }

        if (!client.grants.includes(grantType)) {
            throw new UnauthorizedClientError(
                "Unauthorized client: `grantType` is invalid",
            )
        }

        const accessTokenLifetime = this.getAccessTokenLifetime(client)
        const refreshTokenLifetime = this.getRefreshTokenLifetime(client)
        const GrantType = this.grantTypes[grantType]

        const options = {
            accessTokenLifetime,
            model: this.model,
            refreshTokenLifetime,
            alwaysIssueNewRefreshToken: this.alwaysIssueNewRefreshToken,
        }

        return new GrantType(options).handle(request, client)
    }

    /**
     * Get access token lifetime.
     */

    getAccessTokenLifetime(client: Client) {
        return client.accessTokenLifetime || this.accessTokenLifetime
    }

    /**
     * Get refresh token lifetime.
     */

    getRefreshTokenLifetime(client: Client) {
        return client.refreshTokenLifetime || this.refreshTokenLifetime
    }

    /**
     * Get token type.
     */

    getTokenType(model: any) {
        return new BearerTokenType(
            model.accessToken,
            model.accessTokenLifetime,
            model.refreshToken,
            model.scope,
            model.user,
            model.customAttributes,
        )
    }

    /**
     * Update response when a token is generated.
     */

    updateSuccessResponse(response: Response, tokenType: BearerTokenType) {
        response.body = tokenType.valueOf()

        response.set("Cache-Control", "no-store")
        response.set("Pragma", "no-cache")
    }

    /**
     * Update response when an error is thrown.
     */

    updateErrorResponse(response: Response, error: OAuthError) {
        response.body = {
            error: error.name,
            error_description: error.message,
        }

        response.status = error.code
    }

    /**
     * Given a grant type, check if client authentication is required
     */
    isClientAuthenticationRequired(grantType: string) {
        if (Object.keys(this.requireClientAuthentication).length > 0) {
            return typeof this.requireClientAuthentication[grantType] !== "undefined"
                ? this.requireClientAuthentication[grantType]
                : true
        }

        return true
    }
}
