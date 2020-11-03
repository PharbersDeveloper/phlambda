import * as fs from "fs"
import moment from "moment"

test(
    "OAuth Login",
    async () => {
        const event = JSON.parse(fs.readFileSync("../events/event_oauth_login.json", "utf8"))
        const app = require("../../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(200)
        expect(typeof res.body).toEqual("string")
        expect(JSON.parse(res.body).message).toBe("login success")
        console.info(JSON.parse(res.body))
    },
    1000 * 60 * 2,
)

test(
    "OAuth Authorization",
    async () => {
        const event = JSON.parse(fs.readFileSync("../events/event_oauth_authorization.json", "utf8"))
        event.queryStringParameters.user_id = "APqnkJ2TjdeYG-gsc9n8"
        const app = require("../../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(200)
        expect(typeof res.body).toEqual("string")
        expect(res.body.includes("code")).toEqual(true)
        console.info(res.body)
    },
    1000 * 60 * 2,
)

// test("OAuth Token", async () => {
//     const event = JSON.parse(fs.readFileSync("../events/event_oauth_token.json", "utf8"))
//     event.queryStringParameters.code = "0f94d8bf747adf47da64663b008f8274e50e82c3c8858f133c400f7b270102af"
//     const app = require("../../app.js")
//     const res = await app.lambdaHandler(event, undefined)
//     expect(res.statusCode).toBe(200)
//     expect(typeof res.body).toEqual("string")
//     expect("access_token" in JSON.parse(res.body)).toEqual(true)
//     console.info(res)
// }, 5000)
