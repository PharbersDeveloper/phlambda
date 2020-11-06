import * as fs from "fs"

const AgentAccess = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_login.json", "utf8"))
    event.queryStringParameters.client_id = "fjjnl2uSalHTdrppHG9u"
    event.queryStringParameters.redirect_uri = "http://www.pharbers.com/oauth-callback"
    event.queryStringParameters.client_secret = "2a21aaa08c78eb6f8c7350ac0dbf5f4a823754915c6302cf2ae6b93ac6caa6e2"
    return event
})

const AgentClientError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_login.json", "utf8"))
    event.queryStringParameters.client_id = "error client id"
    event.queryStringParameters.redirect_uri = "http://www.pharbers.com/oauth-callback"
    event.queryStringParameters.client_secret = "2a21aaa08c78eb6f8c7350ac0dbf5f4a823754915c6302cf2ae6b93ac6caa6e2"
    return event
})

const AgentSecretError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_login.json", "utf8"))
    event.queryStringParameters.client_id = "fjjnl2uSalHTdrppHG9u"
    event.queryStringParameters.redirect_uri = "http://www.pharbers.com/oauth-callback"
    event.queryStringParameters.client_secret = "error secret"
    return event
})

const AgentRedirectUriError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_login.json", "utf8"))
    event.queryStringParameters.client_id = "fjjnl2uSalHTdrppHG9u"
    event.queryStringParameters.redirect_uri = ""
    event.queryStringParameters.client_secret = "2a21aaa08c78eb6f8c7350ac0dbf5f4a823754915c6302cf2ae6b93ac6caa6e2"
    return event
})

const AgentException = jest.fn(() => {
    return new Map()
})

test("Agent Access", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new AgentAccess(), undefined)
    expect(res.statusCode).toBe(200)
    expect(typeof res.body).toEqual("string")
    expect(res.body).toContain("DOCTYPE")
}, 1000 * 60 * 2)

test("Agent ClientID Error", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new AgentClientError(), undefined)
    expect(res.statusCode).toBe(403)
    expect(typeof res.body).toEqual("string")
    expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid client, please contact pharbers")
}, 1000 * 60 * 2)

test("Agent Secret Error", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new AgentSecretError(), undefined)
    expect(res.statusCode).toBe(501)
    expect(typeof res.body).toEqual("string")
    expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid parameters")
}, 1000 * 60 * 2)

test("Agent RedirectUri Error By Null", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new AgentRedirectUriError(), undefined)
    expect(res.statusCode).toBe(501)
    expect(typeof res.body).toEqual("string")
    expect(JSON.parse(res.body).message.toLowerCase()).toBe("invalid parameters")
}, 1000 * 60 * 2)

test("Agent Error By Exception", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new AgentException(), undefined)
    expect(typeof res).toEqual("object")
    console.info(JSON.stringify(res))
}, 1000 * 60 * 2)
