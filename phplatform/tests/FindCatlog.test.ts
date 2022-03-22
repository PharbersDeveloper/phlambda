import * as fs from "fs"
import { Logger } from "phnodelayer"

const FindTemplate = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("events/Find_Template.json", "utf-8"))
    event.path = "/phplatfrom/catlog"
    event.httpMethod = "POST"
    event.body = JSON.stringify({
        projectId: "aaaa",
        dsName: "A"
    })
    event.pathParameters = {
        type: "catlog"
    }
    return event
})

describe("Find Data", () => {
    beforeAll(async () => {
        // process.env.AWS_ACCESS_KEY_ID = "ASIAWPBDTVEAPRFT756L"
        // process.env.AccessKeyId = "ASIAWPBDTVEAPRFT756L"
        // process.env.AWS_SECRET_ACCESS_KEY = "t1QfpPuTZzakt8/i0+R6AAcFU4Qsai5Jie9P87TI"
        // process.env.SecretAccessKey = "t1QfpPuTZzakt8/i0+R6AAcFU4Qsai5Jie9P87TI"
    })

    test("Find Catlog", async () => {
        const event = new FindTemplate()
        const app = require("../app.js")
        const result = await app.lambdaHandler(event, undefined)
        expect(result.statusCode).toBe(200)
    })
})
