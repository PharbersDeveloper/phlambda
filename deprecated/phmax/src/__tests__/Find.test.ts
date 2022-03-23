import * as fs from "fs"
import { Logger } from "phnodelayer"

const FindMaxFunctions = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/max/event_max_find.json", "utf8"))
})

const FindTableSchema = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/max/event_max_find_table.json", "utf8"))
})

describe("Find Test", () => {
    let config
    beforeAll(async () => {
        process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
        process.env.SecretAccessKey = "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"
    })

    test("Find Max", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindMaxFunctions(), undefined)
        Logger.info(result)
    })

})
