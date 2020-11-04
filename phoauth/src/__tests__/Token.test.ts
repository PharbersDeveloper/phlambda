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
        event.queryStringParameters.user_id = "qtaGDePl1OrSFEgm"
        const app = require("../../app.js")
        const res = await app.lambdaHandler(event, undefined)
        expect(res.statusCode).toBe(200)
        expect(typeof res.body).toEqual("string")
        expect(res.body.includes("code")).toEqual(true)
        console.info(res.body)
    },
    1000 * 60 * 2,
)

test("OAuth Token", async () => {
    const event = JSON.parse(fs.readFileSync("../events/event_oauth_token.json", "utf8"))
    event.queryStringParameters.code = "a1748c283c2a0a30ce5d1e83b6008e534558a38ecd0332e3872655b90178e49b"
    const app = require("../../app.js")
    const res = await app.lambdaHandler(event, undefined)
    expect(res.statusCode).toBe(200)
    expect(typeof res.body).toEqual("string")
    expect("access_token" in JSON.parse(res.body)).toEqual(true)
    console.info(res)
}, 5000)
