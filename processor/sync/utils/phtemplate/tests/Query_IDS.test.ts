import * as fs from "fs"
import { Logger } from "phnodelayer"

const IDSTemplate = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/IDS_Template.json", "utf-8")))

describe("IDS", () => {
    test("Query", async () => {
        const app = require("../app.js")
        const result = await app.lambdaHandler(IDSTemplate(), undefined)
        Logger.info(result)
        expect(JSON.parse(result.body).data instanceof Array).toBe(true)
    })
})
