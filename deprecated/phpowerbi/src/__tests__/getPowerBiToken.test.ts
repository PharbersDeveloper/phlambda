import * as fs from "fs"

test("Get Power BI Token App", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_power_bi.json", "utf8"))
    const app = require("../../app.js")
    const res = await app.lambdaHandler(event, undefined)
    // tslint:disable-next-line:no-console
    console.debug(res)
}, 5000)
