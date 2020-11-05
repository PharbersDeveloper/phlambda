import * as fs from "fs"

const OAuthAccess = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_token.json", "utf8"))
    event.queryStringParameters.code = "d1e70ffe8e9ecbe0fe3d08bf56786fd6d9c44d5793eb91dc928581bd2a6cf536"
    event.queryStringParameters.redirect_uri = "www.pharbers.com"
    event.queryStringParameters.client_id = "V5I67BHIRVR2Z59kq-a-"
    event.queryStringParameters.grant_type = "authorization_code"
    return event
})

const OAuthGenerateClientIdError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_token.json", "utf8"))
    event.queryStringParameters.code = "147de1c34e11636ea6f0814f01c1bf15ef0c4477f2f6cdb5304c0c66178e8763"
    event.queryStringParameters.redirect_uri = "www.pharbers.com"
    event.queryStringParameters.client_id = "clientid0x1"
    event.queryStringParameters.grant_type = "authorization_code"
    return event
})

const OAuthGenerateCodeError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_token.json", "utf8"))
    event.queryStringParameters.code = "coodeerror"
    event.queryStringParameters.redirect_uri = "www.pharbers.com"
    event.queryStringParameters.client_id = "V5I67BHIRVR2Z59kq-a-"
    event.queryStringParameters.grant_type = "authorization_code"
    return event
})

const OAuthGenerateGrantTypeError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_token.json", "utf8"))
    event.queryStringParameters.code = "147de1c34e11636ea6f0814f01c1bf15ef0c4477f2f6cdb5304c0c66178e8763"
    event.queryStringParameters.redirect_uri = "www.pharbers.com"
    event.queryStringParameters.client_id = "V5I67BHIRVR2Z59kq-a-"
    event.queryStringParameters.grant_type = "xauthorization_code"
    return event
})

test("OAuth Generate Token Access", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new OAuthAccess(), undefined)
    expect(res.statusCode).toBe(200)
    expect(typeof res.body).toEqual("string")
    expect("access_token" in JSON.parse(res.body)).toEqual(true)
}, 5000)

test("OAuth Generate Token ClientId Error", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new OAuthGenerateClientIdError(), undefined)
    expect(res.statusCode).toBe(404)
    expect(typeof res.body).toEqual("string")
    expect(JSON.parse(res.body).message.toLowerCase()).toBe("record not found")
}, 5000)

test("OAuth Generate Token Code Error", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new OAuthGenerateCodeError(), undefined)
    expect(res.statusCode).toBe(501)
    expect(typeof res.body).toEqual("string")
    expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid parameters")
}, 5000)

test("OAuth Generate Token GrantType Error", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new OAuthGenerateGrantTypeError(), undefined)
    expect(res.statusCode).toBe(403)
    expect(typeof res.body).toEqual("string")
    expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid grant type")
}, 5000)
