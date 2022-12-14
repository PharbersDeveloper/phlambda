import * as fs from "fs"

const GETAllow = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_token_auth.json", "utf8"))
    event.type = "TOKEN"
    event.authorizationToken = "c9418a2c66bf83a690a2f7d3f459b34d08ac5ac6c92afc32bd4bdd637e537bad"
    event.methodArn = event.methodArn + "/v0/GET/entry/assets/xxxx"
    return event
})

const POSTAllow = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_token_auth.json", "utf8"))
    event.type = "TOKEN"
    event.authorizationToken = "c9418a2c66bf83a690a2f7d3f459b34d08ac5ac6c92afc32bd4bdd637e537bad"
    event.methodArn = event.methodArn + "/v0/POST/entry/assets/xxxx"
    return event
})

const PATCHAllow = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_token_auth.json", "utf8"))
    event.type = "TOKEN"
    event.authorizationToken = "c9418a2c66bf83a690a2f7d3f459b34d08ac5ac6c92afc32bd4bdd637e537bad"
    event.methodArn = event.methodArn + "/v0/PATCH/entry/assets/xxxx"
    return event
})

const DELETEDeny = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_token_auth.json", "utf8"))
    event.type = "TOKEN"
    event.authorizationToken = "c9418a2c66bf83a690a2f7d3f459b34d08ac5ac6c92afc32bd4bdd637e537bad"
    event.methodArn = event.methodArn + "/v0/DELETE/entry/assets/xxxx"
    return event
})

const TokenError = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_token_auth.json", "utf8"))
    event.type = "TOKEN"
    event.authorizationToken = "error token"
    event.methodArn = event.methodArn + "/v0/DELETE/entry/assets/xxxx"
    return event
})

test("APIGateway GET Allow", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new GETAllow(), undefined)
    expect(typeof res).toBe("object")
    expect(res.principalId).not.toBe("undefined")
    expect(res.policyDocument.Statement.length).toBe(1)
    expect(res.policyDocument.Statement[0].Effect).toBe("Allow")
    console.info(JSON.stringify(res))
}, 1000 * 60 * 2)

test("APIGateway POST Allow", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new POSTAllow(), undefined)
    expect(typeof res).toBe("object")
    expect(res.principalId).not.toBe("undefined")
    expect(res.policyDocument.Statement.length).toBe(1)
    expect(res.policyDocument.Statement[0].Effect).toBe("Allow")
    console.info(JSON.stringify(res))
}, 1000 * 60 * 2)

test("APIGateway PATCH Allow", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new PATCHAllow(), undefined)
    expect(typeof res).toBe("object")
    expect(res.principalId).not.toBe("undefined")
    expect(res.policyDocument.Statement.length).toBe(1)
    expect(res.policyDocument.Statement[0].Effect).toBe("Allow")
    console.info(JSON.stringify(res))
}, 1000 * 60 * 2)

test("APIGateway DELETE Deny", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new DELETEDeny(), undefined)
    expect(typeof res).toBe("object")
    expect(res.principalId).not.toBe("undefined")
    expect(res.policyDocument.Statement.length).toBe(1)
    expect(res.policyDocument.Statement[0].Effect).toBe("Deny")
    console.info(JSON.stringify(res))
}, 1000 * 60 * 2)

test("APIGateway Token Error Deny", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new TokenError(), undefined)
    expect(typeof res).toBe("object")
    expect(res.principalId).toBe("undefined")
    expect(res.policyDocument.Statement.length).toBe(1)
    expect(res.policyDocument.Statement[0].Effect).toBe("Deny")
    console.info(JSON.stringify(res))
}, 1000 * 60 * 2)
