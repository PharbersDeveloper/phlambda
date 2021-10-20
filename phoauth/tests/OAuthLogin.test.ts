import * as fs from "fs"

const LoginTemplate = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/OAuth2_Login.json", "utf-8")))

describe("Login Test", () => {
    let event
    beforeAll(() => event = new LoginTemplate())

    test("Login Access", async () => {
        event.queryStringParameters.email = "pqian@pharbers.com"
        event.queryStringParameters.password = "1cd7fc9d631b3541354d5119236bae5f668e02e7c9472d9f0f56f83ccf2bc582"
        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(200)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message).toBe("login success")
    })

    test("Login Account Error", async () => {
        event.queryStringParameters.email = "alex123@pharbers.com"
        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(404)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toBe("record not found")
    })

    test("Login Password Error", async () => {
        event.queryStringParameters.email = "pqian@pharbers.com"
        event.queryStringParameters.password = "a12"
        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(403)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message.toLowerCase()).toBe("username or password is not valid")
    })
})
