import * as fs from "fs"

const OAuthAccess = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.token.json", "utf8"))
    event.httpMethod = "POST"
    event.headers.authorization = "Basic WHdneHRhRlRocWZKNGxydS1hLTo5NjFlZDRhZDg0MjE0N2E1YzlhMWNiYzYzMzY5MzQzOGUxZjRhOGViYjcxMDUwZDlkOWY3YzQzZGJhZGY5Yjcy"
    event.headers.accept = "application/x-www-form-urlencoded"
    event.headers["content-type"] = "application/x-www-form-urlencoded"
    const code = "9762717268e814b8f61e536a9887248af4c5db36ba93b98738cdb8e474806974"
    event.body = `code=${code}&grant_type=authorization_code&redirect_uri=http%3A%2F%2Fgeneral.pharbers.com%2Foauth-callback`
    return event
})

const OAuthGenerateClientIdError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.token.json", "utf8"))
    event.httpMethod = "POST"
    event.headers.authorization = "Basic Y2xpZW50aWQweDE6OTYxZWQ0YWQ4NDIxNDdhNWM5YTFjYmM2MzM2OTM0MzhlMWY0YThlYmI3MTA1MGQ5ZDlmN2M0M2RiYWRmOWI3Mg=="
    event.headers.accept = "application/x-www-form-urlencoded"
    event.headers["content-type"] = "application/x-www-form-urlencoded"
    const code = "9762717268e814b8f61e536a9887248af4c5db36ba93b98738cdb8e474806974"
    event.body = `code=${code}&grant_type=authorization_code&redirect_uri=http%3A%2F%2Fgeneral.pharbers.com%2Foauth-callback`
    return event
})

const OAuthGenerateCodeError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.token.json", "utf8"))
    event.httpMethod = "POST"
    event.headers.authorization = "Basic WHdneHRhRlRocWZKNGxydS1hLTo5NjFlZDRhZDg0MjE0N2E1YzlhMWNiYzYzMzY5MzQzOGUxZjRhOGViYjcxMDUwZDlkOWY3YzQzZGJhZGY5Yjcy"
    event.headers.accept = "application/x-www-form-urlencoded"
    event.headers["content-type"] = "application/x-www-form-urlencoded"
    const code = "coodeerror"
    event.body = `code=${code}&grant_type=authorization_code&redirect_uri=http%3A%2F%2Fgeneral.pharbers.com%2Foauth-callback`
    return event
})

const OAuthGenerateGrantTypeError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.token.json", "utf8"))
    event.httpMethod = "POST"
    event.headers.authorization = "Basic WHdneHRhRlRocWZKNGxydS1hLTo5NjFlZDRhZDg0MjE0N2E1YzlhMWNiYzYzMzY5MzQzOGUxZjRhOGViYjcxMDUwZDlkOWY3YzQzZGJhZGY5Yjcy"
    event.headers.accept = "application/x-www-form-urlencoded"
    event.headers["content-type"] = "application/x-www-form-urlencoded"
    const code = "9762717268e814b8f61e536a9887248af4c5db36ba93b98738cdb8e474806974"
    event.body = `code=${code}&grant_type=xauthorization_code&redirect_uri=http%3A%2F%2Fgeneral.pharbers.com%2Foauth-callback`
    return event
})

describe("OAuth Token Test", () => {
    test("OAuth Generate Token ClientId Error", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new OAuthGenerateClientIdError(), undefined)
        expect(res.statusCode).toBe(401)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid client: client is invalid")
    }, 5000)

    test("OAuth Generate Token Code Error", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new OAuthGenerateCodeError(), undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid grant: authorization code is invalid")
    }, 5000)

    test("OAuth Generate Token GrantType Error", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new OAuthGenerateGrantTypeError(), undefined)
        expect(res.statusCode).toBe(400)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toBe("unsupported grant type: `granttype` is invalid")
    }, 5000)

    test("OAuth Generate Token Access", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new OAuthAccess(), undefined)
        expect(res.statusCode).toBe(200)
        expect(typeof res.body).toEqual("string")
        expect("access_token" in JSON.parse(res.body)).toEqual(true)
    }, 5000)
})
