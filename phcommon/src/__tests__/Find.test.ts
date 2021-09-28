import * as fs from "fs"

const FindAccountsEvent = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/common/event_common_find.json", "utf8"))
})

describe("Common Find Test", () => {
    test("Find Accounts", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindAccountsEvent(), undefined)
        expect(result.statusCode).toBe(200)
    })
})
