import * as fs from "fs"

const HookContext = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_find.json", "utf8"))
    // event.queryStringParameters.
    return event
})

test("Hook Context", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new HookContext(), undefined)
    // tslint:disable-next-line:no-console
    console.info(JSON.stringify(JSON.parse(res.body)))
}, 1000 * 60 * 2)
