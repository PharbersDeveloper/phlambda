import * as fs from "fs"

const FindFilterTableSuccess = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/catlog/catlog_find_table.json", "utf8"))
})

test("Find Tables For DataBaseName Success", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new FindFilterTableSuccess(), undefined)
    console.info(result)
}, 1000 * 60 * 10)
