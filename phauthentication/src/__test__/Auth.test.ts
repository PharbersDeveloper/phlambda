import * as fs from "fs"

test("APIGateway Simple Test", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_token_auth.json", "utf8"))
    const app = require("../../app.js")
    const res = await app.lambdaHandler(event, undefined)
    console.info(res)
}, 1000 * 60 * 2)
