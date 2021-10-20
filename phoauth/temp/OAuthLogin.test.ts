import * as fs from "fs"

const LoginAccessEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.login.json", "utf8"))
    event.queryStringParameters.email = "pqian@pharbers.com"
    event.queryStringParameters.password = "1cd7fc9d631b3541354d5119236bae5f668e02e7c9472d9f0f56f83ccf2bc582"
    return event
})

const LoginAccountErrorEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.login.json", "utf8"))
    event.queryStringParameters.email = "alex@pharbers.com"
    return event
})

const LoginPasswordErrorEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth/oauth2.login.json", "utf8"))
    event.queryStringParameters.email = "pqian@pharbers.com"
    event.queryStringParameters.password = "a12"
    return event
})

describe("OAuth Login Test", () => {
    test("OAuth Login Access", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new LoginAccessEvent(), undefined)
        expect(res.statusCode).toBe(200)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message).toBe("login success")
    }, 1000 * 60 * 2)

    test("OAuth Login Account Error", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new LoginAccountErrorEvent(), undefined)
        expect(res.statusCode).toBe(404)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toBe("record not found")
    }, 5000)

    test("OAuth Login Password Error", async () => {
        const app = require("../app.js")
        const res = await app.lambdaHandler(new LoginPasswordErrorEvent(), undefined)
        expect(res.statusCode).toBe(403)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toBe("username or password is not valid")
    }, 5000)
})
