import * as fs from "fs"
import { Logger } from "phnodelayer"

process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
process.env.SecretAccessKey = "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"

const CreateStepFunction = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/project/stepfunction_execution_create.json", "utf8"))
})

describe("Create Test", () => {
    test("Create Execution", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new CreateStepFunction(), undefined)
        Logger.info(result)
    }, 1000 * 60)
})
