
import * as fs from "fs"
import { Logger } from "phnodelayer"
import { Http } from "../common/http"
import Shell from "../common/shell"

import AppLambdaDelegate from "../delegate/appLambdaDelegate"

test("call python phcli success", async () => {
    const del = new AppLambdaDelegate()
    await del.exec(null)
})

test("call python phcli parameter error", async () => {
    const del = new AppLambdaDelegate()
    await del.exec(null)
})

test("call python phcli event is null", async () => {
    const del = new AppLambdaDelegate()
    await del.exec(null)
})

test("shell test", async () => {
    const result = await new Http().post("http://airflow.pharbers.com/api/v1/dags/A/dagRuns", {conf: {name: "Alex"}})
    Logger.info(result)
    const cmd = "echo \"python3\"|phcli maxauto --cmd create --path AlexTest"
    const { error, stdout, stderr } = await Shell.getIns.cmd(cmd).exec()
    Logger.info(error)
    Logger.info(stdout)
    Logger.info(stderr)
})

test("call airflow http app.js", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_act_forgotPassword.json", "utf8"))
    event.body = "{\"data\": {  \"type\": \"triggers\", \"attributes\": { \"timeLeft\": \"F\", \"timeRight\": \"B\", \"email\":\"aa@aa.pha.com\", \"atc\": null }} }"
    event.httpMethod = "POST"
    event.resource = "/phproject/{type}"
    event.path = "/phproject/triggers"
    event.pathParameters = {
        type: "triggers"
    }
    const app = require("../../app.js")
    const res = await app.lambdaHandler(event, undefined)
    Logger.info(res)
})
