import * as fs from "fs"

const FindDataBaseAllSuccess = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/catlog/catlog_find_database.json", "utf8"))
})

test("Find DataBase All Data Success", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new FindDataBaseAllSuccess(), undefined)
    console.info(result)
}, 1000 * 60 * 10)
