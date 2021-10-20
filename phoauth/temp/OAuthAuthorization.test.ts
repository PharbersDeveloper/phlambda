import * as fs from "fs"

const AuthAccessEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.authorize.json", "utf8"))
    event.queryStringParameters.response_type = "code"
    event.queryStringParameters.client_id = "XwgxtaFThqfJ4lru-a-"
    event.queryStringParameters.user_id = "8m6H9cKoskgEfn0v"
    event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
    event.queryStringParameters.state = "state"
    return event
})

const AuthAccountError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.authorize.json", "utf8"))
    event.queryStringParameters.response_type = "code"
    event.queryStringParameters.client_id = "V5I67BHIRVR2Z59kq-a-"
    event.queryStringParameters.user_id = "aaaa"
    event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
    event.queryStringParameters.state = "state"
    return event
})

const AuthResponseTypeError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.authorize.json", "utf8"))
    event.queryStringParameters.response_type = "xcode"
    event.queryStringParameters.client_id = "V5I67BHIRVR2Z59kq-a-"
    event.queryStringParameters.user_id = "qtaGDePl1OrSFEgm"
    event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
    event.queryStringParameters.state = "state"
    return event
})

const AuthClientIdError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.authorize.json", "utf8"))
    event.queryStringParameters.response_type = "code"
    event.queryStringParameters.client_id = "clientidx01"
    event.queryStringParameters.user_id = "qtaGDePl1OrSFEgm"
    event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
    event.queryStringParameters.state = "state"
    return event
})

const AuthClientIdExpiredError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.authorize.json", "utf8"))
    event.queryStringParameters.response_type = "code"
    event.queryStringParameters.client_id = "9PcCqezidynO1I0U"
    event.queryStringParameters.user_id = "qtaGDePl1OrSFEgm"
    event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
    event.queryStringParameters.state = "state"
    return event
})

const AuthScopeError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.authorize.json", "utf8"))
    event.queryStringParameters.response_type = "code"
    event.queryStringParameters.client_id = "V5I67BHIRVR2Z59kq-a-"
    event.queryStringParameters.user_id = "qtaGDePl1OrSFEgm"
    event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
    event.queryStringParameters.scope = "error scope"
    event.queryStringParameters.state = "state"
    return event
})

describe("OAuth Authorization Test", () => {
    test("OAuth Generate Authorization Code Access", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new AuthAccessEvent(), undefined)
        expect(res.statusCode).toBe(200)
        expect(typeof res.body).toEqual("string")
        expect(res.body.includes("code")).toEqual(true)
    }, 5000)

    test("OAuth Generate Authorization Code UserId Error", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new AuthAccountError(), undefined)
        expect(res.statusCode).toBe(302)
        expect(res.body).toEqual("{}")
        expect(typeof res.headers.location).toEqual("string")
    }, 5000)

    test("OAuth Generate Authorization Code ResponseType Error", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new AuthResponseTypeError(), undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toBe("unsupported response type: `responsetype` is not supported")
    }, 5000 * 60)

    test("OAuth Generate Authorization Code ClientId Error", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new AuthClientIdError(), undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        // expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid client, please contact pharbers")
    }, 5000)

    test("OAuth Generate Authorization Code ClientId Expired Error", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new AuthClientIdExpiredError(), undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        // expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid client, please contact pharbers")
    }, 5000)

    test("OAuth Generate Authorization Code Scope Error", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new AuthScopeError(), undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        // expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid scope grant")
    }, 5000)
})

