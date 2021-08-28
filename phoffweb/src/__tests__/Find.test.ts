import * as fs from "fs"

const FindReportsEvent = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/offweb/event_offweb_find.json", "utf8"))
})

describe("Find Test", () => {
    test("Find Reports", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new FindReportsEvent(), undefined)
        expect(result.statusCode).toBe(200)
    })
})
