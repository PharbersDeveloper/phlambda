import * as fs from "fs"

const FindEvent = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/report/event_reports_find.json", "utf8"))
})

describe("Find Test", () => {
    test("Find Report", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindEvent(), undefined)
        expect(result.statusCode).toBe(200)
    })
})
