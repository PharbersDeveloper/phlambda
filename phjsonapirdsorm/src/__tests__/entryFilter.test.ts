import * as fs from "fs"

const HookContext = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/entry/event_entry_filter_asset.json", "utf8"))
})

describe("Entry Test", () => {
    test("Filter", async () => {
        const app = require("../../app.js")
        const res = await app.lambdaHandler(new HookContext(), undefined)
        // tslint:disable-next-line:no-console
        console.info(res.body)
    }, 1000 * 60 * 10)
})
