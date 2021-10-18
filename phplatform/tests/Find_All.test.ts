import * as fs from "fs"
import { Logger } from "phnodelayer"
import { AWSRegion } from "../src/constants/common"
import AWSSts from "../src/utils/AWSSts"

const FindTemplate = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/Find_Template.json", "utf-8")))

describe("Find All Entity", () => {

    beforeAll(async () => {
        // 因部分代码需要aws的角色权限，既：有了获取临时token的code
        const sts = new AWSSts(
            "AKIAWPBDTVEAI6LUCLPX",
            "Efi6dTMqXkZQ6sOpmBZA1IO1iu3rQyWAbvKJy599",
            AWSRegion)

        const { region, credentials: { accessKeyId, secretAccessKey, sessionToken }} = await sts.assumeRole(
            "Pharbers-ETL-Roles",
            "arn:aws-cn:iam::444603803904:role/Pharbers-ETL-Roles")

        process.env.AWS_DEFAULT_REGION = region
        process.env.AWS_ACCESS_KEY_ID = accessKeyId
        process.env.AWS_SECRET_ACCESS_KEY = secretAccessKey
        process.env.AWS_SESSION_TOKEN = sessionToken
    })

    // Tables
    const entities = [
        "activities", "images", "reports", "participants",
        "cooperations", "events", "zones", "files",
        "diagrams", "dbs", "tables", "resources",
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
