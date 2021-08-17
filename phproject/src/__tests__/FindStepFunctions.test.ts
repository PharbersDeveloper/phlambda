
import * as fs from "fs"
import { Logger } from "phnodelayer"

const FindStepFunctions = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/project/stepfunction_project_find.json", "utf8"))
})

const FindStepFunctionByID = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/project/stepfunction_project_by_id.json", "utf8"))
})

const FindStepFunctionInclude = jest.fn( () => {
    return JSON.parse(fs.readFileSync("../events/project/stepfunction_project_find_include.json", "utf8"))
})

const FindStepFunctionExecutions = jest.fn( () => {
    return JSON.parse(fs.readFileSync("../events/project/stepfunction_execution_find.json", "utf8"))
})

process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
process.env.SecretAccessKey = "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"

describe("StepFunctions Test", () => {
    test("Find Step Functions", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindStepFunctions(), undefined)
        Logger.info(result)
        expect(result.statusCode).toBe(200)
    }, 1000 * 60 * 10)

    test("Find Step Functions By ID", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindStepFunctionByID(), undefined)
        expect(result.statusCode).toBe(200)
        Logger.info(result)
    }, 1000 * 60 * 10)

    test("Find Step Functions Include", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindStepFunctionInclude(), undefined)
        expect(result.statusCode).toBe(200)
        Logger.info(result)
    }, 1000 * 60 * 10)

    test("Find Step Functions Executions", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindStepFunctionExecutions(), undefined)
        expect(result.statusCode).toBe(200)
        Logger.info(result)
    }, 1000 * 3)
})
