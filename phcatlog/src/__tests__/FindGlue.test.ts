
import * as fs from "fs"

const FindDataBaseEvent = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/catlog/catlog_find_database.json", "utf8"))
})

const FindDataBaseTableEvent = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/catlog/catlog_find_table.json", "utf8"))
})

const FindPagePartitionEvent = jest.fn( () => {
    return JSON.parse(fs.readFileSync("../events/catlog/catlog_find_partition.json", "utf8"))
})

process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
process.env.SecretAccessKey = "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"

describe("Find Glue Test", () => {
    test("Find DataBaseAll", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindDataBaseEvent(), undefined)
        console.info(JSON.stringify(JSON.parse(result)))
    }, 1000 * 60 * 10)

    test("Find DataBase Table", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindDataBaseTableEvent(), undefined)
        console.info(JSON.stringify(JSON.parse(result.body)))
    }, 1000 * 60 * 10)

    test("Find Page Partitions", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindPagePartitionEvent(), undefined)
        console.info(result)
    }, 1000 * 60 * 10)
})
