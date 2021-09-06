import * as fs from "fs"
import { Logger } from "phnodelayer"
import { AWSRegion } from "../constants/common"
import GlueCatlogHandler from "../handler/GlueCatlogHandler"
import AWSSts from "../utils/AWSSts"

const awsConfig = jest.fn(async () => {
    const name = "Pharbers-ETL-Roles"
    const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey, AWSRegion)
    return await sts.assumeRole(name, `arn:aws-cn:iam::444603803904:role/${name}`)
})

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
        config = await new awsConfig()
    })

    test("Find Max", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindMaxFunctions(), undefined)
        Logger.info(result)
    })

    test("Find Table Schema", async () => {
        const event = new FindTableSchema()
        const { table, database } = event.queryStringParameters
        const result = await new GlueCatlogHandler(config).findTable(table, database)
        Logger.info(result)
    }, 1000 * 60 * 10)
})
