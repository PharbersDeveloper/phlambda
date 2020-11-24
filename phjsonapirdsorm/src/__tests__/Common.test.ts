import * as fs from "fs"
import { Logger } from "phnodelayer"

test("Update Account Password", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_common_patch_one.json", "utf8"))
    const app = require("../../app.js")
    const res = await app.lambdaHandler(event, undefined)
    Logger.info(JSON.parse(String(res.payload)))
}, 5000)

test("Account Find One", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_common_find_one.json", "utf8"))
    const app = require("../../app.js")
    const res = await app.lambdaHandler(event, undefined)
    Logger.info(JSON.parse(String(res.body)))
}, 5000)

test("Account First & Last Name Create", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_common_patch_one.json", "utf8"))
    const app = require("../../app.js")
    const res = await app.lambdaHandler(event, undefined)
    Logger.info(JSON.parse(String(res.body)))
}, 5000)

test("Account Find One", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_common_find_one.json", "utf8"))
    const app = require("../../app.js")
    const res = await app.lambdaHandler(event, undefined)
    Logger.info(JSON.parse(String(res.body)))
}, 1000 * 60 * 2)
