import * as fs from "fs"

const AuthorizationTemplate = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/OAuth2_Authorization.json", "utf-8")))

describe("Authorization Tests", () => {
    let event
    beforeAll(() => event = new AuthorizationTemplate())

    test("Generate Authorization Code Access", async () => {
        event.queryStringParameters.response_type = "code"
        event.queryStringParameters.client_id = "XwgxtaFThqfJ4lru-a-"
        event.queryStringParameters.user_id = "8m6H9cKoskgEfn0v"
        event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
        event.queryStringParameters.state = "state"

        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(200)
        expect(typeof res.body).toEqual("string")
        expect(res.body.includes("code")).toEqual(true)
    })

    test("Generate Authorization Code UserId Error", async () => {
        event.queryStringParameters.response_type = "code"
        event.queryStringParameters.client_id = "V5I67BHIRVR2Z59kq-a-"
        event.queryStringParameters.user_id = "error"
        event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
        event.queryStringParameters.state = "state"

        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(302)
        expect(res.body).toEqual("{}")
        expect(typeof res.headers.location).toEqual("string")
    })

    test("Generate Authorization Code ResponseType Error", async () => {
        event.queryStringParameters.response_type = "xcode"
        event.queryStringParameters.client_id = "V5I67BHIRVR2Z59kq-a-"
        event.queryStringParameters.user_id = "qtaGDePl1OrSFEgm"
        event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
        event.queryStringParameters.state = "state"

        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toEqual("unsupported response type: `responsetype` is not supported")

    })

    test("Generate Authorization Code ClientId Error", async () => {
        event.queryStringParameters.response_type = "code"
        event.queryStringParameters.client_id = "clientidx01"
        event.queryStringParameters.user_id = "qtaGDePl1OrSFEgm"
        event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
        event.queryStringParameters.state = "state"

        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toEqual("invalid client: client credentials are invalid")
        // expect(JSON.parse(res.body).message.toLowerCase()).toEqual("invalid client, please contact pharbers")
    })

    test("Generate Authorization Code ClientId Expired Error", async () => {
        event.queryStringParameters.response_type = "code"
        event.queryStringParameters.client_id = "9PcCqezidynO1I0U"
        event.queryStringParameters.user_id = "qtaGDePl1OrSFEgm"
        event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
        event.queryStringParameters.state = "state"

        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toEqual("invalid client: client credentials are invalid")
        // expect(JSON.parse(res.body).message.toLowerCase()).toEqual("invalid client, please contact pharbers")

    })

    test("Generate Authorization Code Scope Error", async () => {
        event.queryStringParameters.response_type = "code"
        event.queryStringParameters.client_id = "V5I67BHIRVR2Z59kq-a-"
        event.queryStringParameters.user_id = "qtaGDePl1OrSFEgm"
        event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
        event.queryStringParameters.scope = "error scope"
        event.queryStringParameters.state = "state"

        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toEqual("invalid scope: requested scope is invalid")
        // expect(JSON.parse(res.body).message.toLowerCase()).toEqual("invalid scope grant")

    })
})
