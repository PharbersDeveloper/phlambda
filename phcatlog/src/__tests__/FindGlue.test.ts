
import * as fs from "fs"

const FindDataBaseEvent = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/catlog/catlog_find_database.json", "utf8"))
})

process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
process.env.SecretAccessKey = "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"

test("Find DataBaseAll", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new FindDataBaseEvent(), undefined)
    console.info(result)
}, 1000 * 60 * 10)
