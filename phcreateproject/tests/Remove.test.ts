import * as fs from "fs"
import { Logger } from "phnodelayer"
import OptEfsHandler from "../src/handler/optEfsHandler";

const template = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/Create_Template.json", "utf-8")))

describe("Remove Project", () => {
    const app = require("../app.js")

    test("Remove Project", async () => {
        const event = template()
        event.path = "/phcreatereproject/projects/dbtbf08xg1UFE3o"
        event.httpMethod = "DELETE"
        event.resource = "/phcreatereproject/{type}/{id}"
        event.pathParameters = {
            type: "projects",
            id: "dbtbf08xg1UFE3o"
        }
        event.body = ""

        const response = await app.lambdaHandler(event, undefined)
        console.info(response)
    })
})
