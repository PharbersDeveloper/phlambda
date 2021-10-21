import * as fs from "fs"
import { Logger } from "phnodelayer"
import { AWSRegion } from "../src/constants/common"
import AWSSts from "../src/utils/AWSSts"

const FindTemplate = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/Find_Template.json", "utf-8")))

describe("Find All Entity", () => {

    beforeAll(async () => {
        // process.env.AWS_ACCESS_KEY_ID = "AKIAWPBDTVEAPOX3QT6U"
        process.env.AccessKeyId = "AKIAWPBDTVEAPOX3QT6U"
        // process.env.AWS_SECRET_ACCESS_KEY = "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"
        process.env.SecretAccessKey = "Vy7bMX1KCVK9Vow00ovt7r4VmMzhVlpKiE1Cbsor"
    })

    // Tables "dbs", "tables",这个2个表在本地测试，因线上code build不支持assume role
    const entities = [
        "activities", "images", "reports", "participants",
        "cooperations", "events", "zones", "files",
        "diagrams", "resources",
        "projects", "models", "scripts", "datasets",
        "flows", "state-machines", "state-displays", "analysis",
        "notebooks", "dash-boards", "slides", "chats", "wikis"
    ]
    const event = new FindTemplate()
    const app = require("../app.js")

    test("Find All", async () => {
        for ( const item of entities ) {
            Logger.info(item)
            event.path = `/phplatform/${item}`
            event.pathParameters.type = `${item}`
            const result = await app.lambdaHandler(event, undefined)
            expect(result.statusCode).toBe(200)
        }
    }, 1000 * 60)

    test("Find Limit Page Args", async () => {
        const limit = 10
        const offset = 0
        for ( const item of entities ) {
            Logger.info(item)
            event.path = `/phplatform/${item}`
            event.pathParameters.type = `${item}`
            event.queryStringParameters["page[limit]"] = limit
            event.queryStringParameters["page[offset]"] = offset
            const result = await app.lambdaHandler(event, undefined)
            expect(result.statusCode).toBe(200)
            expect(JSON.parse(result.body).data.length).toBeLessThanOrEqual(10)
        }
    }, 1000 * 60)
})
