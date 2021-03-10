import * as fs from "fs"

const temp = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_descpost.json", "utf8"))
    const japi = JSON.stringify({
        data: {
            type: "manufacturers",
            attributes: {
                mnfNameCh: "test",
                mnfType: "test",
                mnfTypeName: "test",
                mnfTypeNameCh: "test",
                corpId: "test",
                corpNameEn: "test",
                corpNameCh: "test",
                location: [0, 0],
                version: "test",
            }
        }
    })
    event.body = japi
    event.path = "/entry/manufacturers"
    event.pathParameters = {
        type: "manufacturers"
    }
    return event
})

test("temp init", async () => {

    const app = require("../../app.js")
    const res = await app.lambdaHandler(new temp(), undefined)
    // tslint:disable-next-line:no-console
    console.info(res.body)

}, 1000 * 60 * 2)
