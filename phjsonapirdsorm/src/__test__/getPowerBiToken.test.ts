import * as fs from "fs"
import { logger } from "phnodelayer"
import bp from "../delegate/appLambdaPowerBiDelegate"

test("Get PowerBI", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_report.json", "utf8"))
    const powerBI = new bp()
    const res = await powerBI.exec(event)
    logger.info(res)
}, 5000)

test("Get Token App", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_report.json", "utf8"))
    const app = require("../../app.js")
    const res = await app.lambdaHandler(event, undefined)
    logger.info(res)
}, 5000)

test("Get Report", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_success_find_one.json", "utf8"))
    const app = require("../../app.js")
    const res = await app.lambdaHandler(event, undefined)
    logger.info(res)
}, 5000)
