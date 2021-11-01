import * as fs from "fs"

const TokenTemplate = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/OAuth2_Password.json", "utf-8")))

describe("Token Password Test", () => {
    let event
    beforeAll(() => {
        event = new TokenTemplate()
    })

    test("Generate Token Access", async () => {
        event.httpMethod = "POST"
        event.headers.authorization = "Basic WHdneHRhRlRocWZKNGxydS1hLTo5NjFlZDRhZDg0MjE0N2E1YzlhMWNiYzYzMzY5MzQzOGUxZjRhOGViYjcxMDUwZDlkOWY3YzQzZGJhZGY5Yjcy"
        event.headers.accept = "application/x-www-form-urlencoded"
        event.headers["content-type"] = "application/x-www-form-urlencoded"
        const grantType = "password"
        const bodys = [
            `grant_type=${grantType}`,
            `redirect_ur=http%3A%2F%2Fgeneral.pharbers.com%2Foauth-callback`,
            `username=pqian@pharbers.com`,
            `password=1cd7fc9d631b3541354d5119236bae5f668e02e7c9472d9f0f56f83ccf2bc582`
        ]
        event.body = bodys.join("&")

        const app = require("../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(200)
        expect(typeof res.body).toEqual("string")
        expect("access_token" in JSON.parse(res.body)).toEqual(true)
    })
})
