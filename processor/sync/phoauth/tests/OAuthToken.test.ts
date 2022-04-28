import * as fs from "fs"

const TokenTemplate = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/OAuth2_Token.json", "utf-8")))

const AuthorizationTemplate = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/OAuth2_Authorization.json", "utf-8")))

describe("Token Test", () => {
    let event
    let authEvent
    let code
    beforeAll(() => {
        event = new TokenTemplate()
        authEvent = new AuthorizationTemplate()
    })

    beforeEach(async () => {
        authEvent.queryStringParameters.response_type = "code"
        authEvent.queryStringParameters.client_id = "XwgxtaFThqfJ4lru-a-"
        authEvent.queryStringParameters.user_id = "8m6H9cKoskgEfn0v"
        authEvent.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
        authEvent.queryStringParameters.state = "state"
        const app = require("../app.js")
        const result = await app.lambdaHandler(authEvent, undefined)
        code = JSON.parse(result.body).redirectUri.split("?")[1].split("&")[0].split("=")[1]
    })

    test("Generate Token Access", async () => {
        event.httpMethod = "POST"
        event.headers.authorization = "Basic WHdneHRhRlRocWZKNGxydS1hLTo5NjFlZDRhZDg0MjE0N2E1YzlhMWNiYzYzMzY5MzQzOGUxZjRhOGViYjcxMDUwZDlkOWY3YzQzZGJhZGY5Yjcy"
        event.headers.accept = "application/x-www-form-urlencoded"
        event.headers["content-type"] = "application/x-www-form-urlencoded"
        event.body = `code=${code}&grant_type=authorization_code&redirect_uri=http%3A%2F%2Fgeneral.pharbers.com%2Foauth-callback`

        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(200)
        expect(typeof res.body).toEqual("string")
        expect("access_token" in JSON.parse(res.body)).toEqual(true)
    })

    test("OAuth Generate Token ClientId Error", async () => {
        event.httpMethod = "POST"
        event.headers.authorization = "Basic Y2xpZW50aWQweDE6OTYxZWQ0YWQ4NDIxNDdhNWM5YTFjYmM2MzM2OTM0MzhlMWY0YThlYmI3MTA1MGQ5ZDlmN2M0M2RiYWRmOWI3Mg=="
        event.headers.accept = "application/x-www-form-urlencoded"
        event.headers["content-type"] = "application/x-www-form-urlencoded"
        event.body = `code=${code}&grant_type=authorization_code&redirect_uri=http%3A%2F%2Fgeneral.pharbers.com%2Foauth-callback`

        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(401)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid client: client is invalid")
    })

    test("Generate Token Code Error", async () => {
        event.httpMethod = "POST"
        event.headers.authorization = "Basic WHdneHRhRlRocWZKNGxydS1hLTo5NjFlZDRhZDg0MjE0N2E1YzlhMWNiYzYzMzY5MzQzOGUxZjRhOGViYjcxMDUwZDlkOWY3YzQzZGJhZGY5Yjcy"
        event.headers.accept = "application/x-www-form-urlencoded"
        event.headers["content-type"] = "application/x-www-form-urlencoded"
        code = "coodeerror"
        event.body = `code=${code}&grant_type=authorization_code&redirect_uri=http%3A%2F%2Fgeneral.pharbers.com%2Foauth-callback`

        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid grant: authorization code is invalid")
    })

    test("Generate Token GrantType Error", async () => {
        event.httpMethod = "POST"
        event.headers.authorization = "Basic WHdneHRhRlRocWZKNGxydS1hLTo5NjFlZDRhZDg0MjE0N2E1YzlhMWNiYzYzMzY5MzQzOGUxZjRhOGViYjcxMDUwZDlkOWY3YzQzZGJhZGY5Yjcy"
        event.headers.accept = "application/x-www-form-urlencoded"
        event.headers["content-type"] = "application/x-www-form-urlencoded"
        event.body = `code=${code}&grant_type=xauthorization_code&redirect_uri=http%3A%2F%2Fgeneral.pharbers.com%2Foauth-callback`

        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toBe("unsupported grant type: `granttype` is invalid")
    })

})
