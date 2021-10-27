import * as fs from "fs"

const VerifyEmailTemplate = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/Verify_Email_Template.json", "utf-8")))

describe("VerifyEmail", () => {
    let event
    beforeAll(() => event = new VerifyEmailTemplate())

    test("Email Succeed", async () => {
        event.queryStringParameters.email = "pqian@pharbers.com"
        const app = require("../app.js")
        const result = await app.lambdaHandler(event, undefined)
        expect(result.statusCode).toBe(200)
        expect(JSON.parse(result.body).status).toEqual("success")
    })

    test("Email Failed", async () => {
        event.queryStringParameters.email = "xxx@xx.com"
        const app = require("../app.js")
        const result = await app.lambdaHandler(event, undefined)
        expect(result.statusCode).toBe(404)
        expect(JSON.parse(result.body).status).toEqual("error")
    })
})
