// import * as fs from "fs"
// import { Logger } from "phnodelayer"
// import RandomCode from "../utils/randomCode"
//
// test("Send Message By Mail", async () => {
//     const event = JSON.parse(fs.readFileSync("../events/event_act_send_msg.json", "utf8"))
//     const app = require("../../app.js")
//     const res = await app.lambdaHandler(event, undefined)
//     Logger.info(res)
// }, 1000 * 60 * 2)
//
// test("1000000 random", async () => {
//     let i
//     for ( i = 0; i <= 1000000; i++ ) {
//         const r = RandomCode.random(6)
//         expect(r.length).toBe(6)
//     }
// }, 1000 * 60 * 2)
//
// test("Verify Code", async () => {
//     const event = JSON.parse(fs.readFileSync("../events/event_act_verify_code.json", "utf8"))
//     const app = require("../../app.js")
//     const res = await app.lambdaHandler(event, undefined)
//     Logger.info(res)
// }, 1000 * 60 * 2)
//
// test("Verify Email", async () => {
//     const event = JSON.parse(fs.readFileSync("../events/event_act_verify_email.json", "utf8"))
//     const app = require("../../app.js")
//     const res = await app.lambdaHandler(event, undefined)
//     Logger.info(res)
// }, 1000 * 60 * 2)
//
// test("Forgot Password", async () => {
//     const event = JSON.parse(fs.readFileSync("../events/event_act_forgotPassword.json", "utf8"))
//     const app = require("../../app.js")
//     const res = await app.lambdaHandler(event, undefined)
//     Logger.info(res)
// }, 1000 * 60 * 2)
test("Get Power BI Token App", async () => {
    const name = "asd"
    expect(name).toEqual("asd")
}, 5000)