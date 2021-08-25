import * as fs from "fs"
import { Logger } from "phnodelayer"

const FindMaxFunctions = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/max/event_max_find.json", "utf8"))
})

describe("Find Test", () => {
    test("Find Max", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindMaxFunctions(), undefined)
        Logger.info(result)
    })
})
