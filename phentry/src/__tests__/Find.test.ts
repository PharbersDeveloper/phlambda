import * as fs from "fs"

const FindAccountsEvent = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/entry/event_entry_find.json", "utf8"))
})

describe("Entry Find Test", () => {
    test("Find Assets", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindAccountsEvent(), undefined)
        expect(result.statusCode).toBe(200)
    })
})
