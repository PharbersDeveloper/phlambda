import * as fs from "fs"
import { logger } from "phnodelayer"

test("Update Account Password", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_common_patch_one.json", "utf8"))
    const app = require("../../app.js")
    const res = await app.lambdaHandler(event, undefined)
    logger.info(JSON.parse(String(res.body)))
}, 5000)
