import * as fs from "fs"

const offweb = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_offweb_find.json", "utf8"))
    // event.queryStringParameters.
    return event
})

test("offweb init", async () => {

    for (const a of [1]) {
        const app = require("../../app.js")
        const res = await app.lambdaHandler(new offweb(), undefined)
        // tslint:disable-next-line:no-console
        console.info(res.body)
    }

}, 1000 * 60 * 2)
