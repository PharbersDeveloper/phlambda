import * as fs from "fs"
import { Logger } from "phnodelayer"

const FindTemplate = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/Find_Template.json", "utf-8")))

describe("Find All, Offweb Entity", () => {
    const entities = ["activities", "images", "reports", "participants", "cooperations", "events", "zones"]
    const event = new FindTemplate()
    const app = require("../../app.js")

    test("Find All", async () => {
        for ( const item of entities ) {
            Logger.info(item)
            event.path = `/phplatform/${item}`
            event.pathParameters.type = `${item}`
            const result = await app.lambdaHandler(event, undefined)
            expect(result.statusCode).toBe(200)
        }
    })

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
    })
})
