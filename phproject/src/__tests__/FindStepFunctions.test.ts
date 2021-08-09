
import * as fs from "fs"

const FindStepFunctionsPage = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/project/stepfunction_find_page.json", "utf8"))
})

const FindOneStepFunction = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/project/stepfunction_find_one.json", "utf8"))
})

process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
process.env.SecretAccessKey = "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"

test("Find Step Functions Page", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new FindStepFunctionsPage(), undefined)
    expect(result.statusCode).toBe(200)
})

test("Find One Step Functions", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new FindOneStepFunction(), undefined)
    expect(result.statusCode).toBe(200)
})

