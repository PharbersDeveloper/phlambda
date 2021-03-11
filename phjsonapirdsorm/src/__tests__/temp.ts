import * as fs from "fs"

const temp = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_descpost.json", "utf8"))
    const japi = JSON.stringify({
        data: {
            type: "descriptions",
            attributes: {
                name: "test",
                source: "aaa",
                createTime: new Date(),
                version: "0.0.1"
            }
        }
    })
    event.body = japi
    return event
})

test("temp init", async () => {

    const app = require("../../app.js")
    const res = await app.lambdaHandler(new temp(), undefined)
    // tslint:disable-next-line:no-console
    console.info(res.body)

}, 1000 * 60 * 2)
