import * as fs from "fs"

const OAuth2ServerEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/oauth2.authorize.json", "utf8"))
    return event
})

test("OAuth2 Server 简单测试", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new OAuth2ServerEvent(), undefined)
    console.info(result)
}, 1000 * 60 * 10)
