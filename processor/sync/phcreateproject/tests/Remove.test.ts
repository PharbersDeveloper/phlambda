import * as fs from "fs"
import { Logger } from "phnodelayer"

const template = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/Create_Template.json", "utf-8")))

describe("Remove Project", () => {
    const app = require("../app.js")

    test("Remove Project", async () => {
        const event = template()
        event.path = "/phcreatereproject/projects/A7t9P78ZBTiyuZc"
        event.httpMethod = "DELETE"
        event.resource = "/phcreatereproject/{type}/{id}"
        event.pathParameters = {
            type: "projects",
            id: "A7t9P78ZBTiyuZc"
        }
        event.body = ""

        const response = await app.lambdaHandler(event, undefined)
        console.info(response)
    })
})
