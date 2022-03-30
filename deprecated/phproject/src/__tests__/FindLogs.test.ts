import * as fs from "fs"
import { Logger } from "phnodelayer"

process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
process.env.SecretAccessKey = "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"

const FindLogsFunction = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/project/stepfunction_find_logs.json", "utf8"))
})

describe("Find Logs", () => {
    test("MapReduce Logs", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindLogsFunction(), undefined)
        Logger.info(result)
    }, 1000 * 60)
})
