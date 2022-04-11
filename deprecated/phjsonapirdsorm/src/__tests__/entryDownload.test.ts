import * as fs from "fs"
import { Logger } from "phnodelayer"
import { entryDownloadHandler } from "../handler/entryDownloadHandler"

test("Download", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(
        JSON.parse(fs.readFileSync("../events/entry/event_entry_download.json", "utf8")),
        undefined)
    Logger.info(res)
}, 1000 * 60 * 2)

