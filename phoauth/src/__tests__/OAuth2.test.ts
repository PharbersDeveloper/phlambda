import * as fs from "fs"

const OAuth2ServerLoginSuccess = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/oauth/oauth2.login.json", "utf8"))
})

const OAuth2ServerAuthorizeSuccess = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.authorize.json", "utf8"))
    event.queryStringParameters.user_id = "5UBSLZvV0w9zh7-lZQap"
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
    const code = "2df5d2f53ea02c7b7f84bc44fa89cb926dcaa2dae4683018f0b53fed152e4e96"
    event.body = `code=${code}&grant_type=authorization_code&redirect_uri=http%3A%2F%2Fgeneral.pharbers.com%2Foauth-callback`
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
    const refreshToken = "61c19f0df715a4f49d08d57be2eb256de03119fae569ae3a0e0b30e1b138b85a"
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
