import * as fs from "fs"
import {logger} from "phnodelayer"

const FindAllAssetsErrorEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_find.json", "utf8"))
    event.path = "/entry/assetsa"
    return event
})

test("Find All Assets", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new FindAllAssetsErrorEvent(), undefined)
    logger.info(res)
}, 1000 * 60 * 2)
