import * as fs from "fs"
import { Logger } from "phnodelayer"

const DBConnection = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
})

test("Test Connection MongoDB", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new DBConnection(), undefined)
    Logger.info(String(result.body))
}, 1000 * 60 * 10)
