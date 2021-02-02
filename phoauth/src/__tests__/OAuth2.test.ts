import * as fs from "fs"

const OAuth2ServerLoginSuccess = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.login.json", "utf8"))
    return event
})

const OAuth2ServerAuthorizeSuccess = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.authorize.json", "utf8"))
    // event.queryStringParameters.user_id = "5UBSLZvV0w9zh7-lZQap"
    event.queryStringParameters.client_id = "V5I67BHIRVR2Z59kq-a-"
    event.queryStringParameters.redirect_uri = "http://general.pharbers.com/oauth-callback"
    event.queryStringParameters.response_type = "code"
    event.queryStringParameters.state = "xyz"
    // event.headers.authorization = "Bearer 6ab197e169268cb40134253705e76ef953b6816eada1f427bb81bf1f775c71d9"
    return event
})

const OAuth2ServerTokenSuccess = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.token.json", "utf8"))
    event.headers.authorization = "Basic VjVJNjdCSElSVlIyWjU5a3EtYS06OTYxZWQ0YWQ4NDIxNDdhNWM5YTFjYmM2MzM2OTM0MzhlMWY0YThlYmI3MTA1MGQ5ZDlmN2M0M2RiYWRmOWI3Mg=="
    event.headers.accept = "application/x-www-form-urlencoded"
    event.headers["content-type"] = "application/x-www-form-urlencoded"
    const code = "200bd5796e41aa090ef94b5d7ac2adef7fd3659fa4744dad3cb77cc6f81250d7"
    event.body = `code=${code}&grant_type=authorization_code&redirect_uri=http://general.pharbers.com/oauth-callback`
    return event
})

const OAuth2ServerMethodGetUserInfo = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.userInfo.json", "utf8"))
    event.headers.authorization = "Bearer b05bb5aa594b55e4f9b3a0ecfeabdb89957728ced5489a29706d75da36fabcd0"
    event.httpMethod = "GET"
    return event
})

const OAuth2ServerMethodPostUserInfo = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.userInfo.json", "utf8"))
    event.headers.authorization = "Bearer b05bb5aa594b55e4f9b3a0ecfeabdb89957728ced5489a29706d75da36fabcd0"
    event.httpMethod = "POST"
    return event
})

const OAuth2ServerRefreshToken = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.refresh_token.json", "utf8"))
    const refreshToken = "50ae8cb9b5566c01268f1d6e1e17aa5bbf8b6322b3a277a50b92107a0fbf40ed"
    event.httpMethod = "POST"
    event.headers.authorization = "Basic VjVJNjdCSElSVlIyWjU5a3EtYS06OTYxZWQ0YWQ4NDIxNDdhNWM5YTFjYmM2MzM2OTM0MzhlMWY0YThlYmI3MTA1MGQ5ZDlmN2M0M2RiYWRmOWI3Mg=="
    event.body = `grant_type=refresh_token&refresh_token=${refreshToken}`
    return event
})

test("OAuth2 Server Login Success", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new OAuth2ServerLoginSuccess(), undefined)
    console.info(result)
}, 1000 * 60 * 10)

test("OAuth2 Server Authorize Success", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new OAuth2ServerAuthorizeSuccess(), undefined)
    console.info(result)
}, 1000 * 60 * 10)

test("OAuth2 Server Token Success", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new OAuth2ServerTokenSuccess(), undefined)
    console.info(result)
}, 1000 * 60 * 10)

test("OAuth2 Server Method Get User Info", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new OAuth2ServerMethodGetUserInfo(), undefined)
    console.info(result)
}, 1000 * 60 * 10)

test("OAuth2 Server Method Post User Info", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new OAuth2ServerMethodPostUserInfo(), undefined)
    console.info(result)
}, 1000 * 60 * 10)

test("OAuth2 Server Refresh Token", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new OAuth2ServerRefreshToken(), undefined)
    console.info(result)
}, 1000 * 60 * 10)
