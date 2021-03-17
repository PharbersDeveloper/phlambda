import * as fs from "fs"
import { Logger } from "phnodelayer"

const answer = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/answers"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "answers"
    }
    return event
})

const evaluation = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/evaluations"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "evaluations"
    }
    return event
})

const final = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/finals"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "finals"
    }
    return event
})

test("Find answer", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new answer(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find evaluations", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new evaluation(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find finals", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new evaluation(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)
