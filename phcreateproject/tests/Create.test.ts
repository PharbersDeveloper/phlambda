import * as fs from "fs"
import { Logger } from "phnodelayer"
import OptEfsHandler from "../src/handler/optEfsHandler";

const template = jest.fn(() =>
    JSON.parse(fs.readFileSync("events/Create_Template.json", "utf-8")))

describe("Create Project", () => {
    const app = require("../app.js")

    test("Create Project", async () => {
        const body = JSON.stringify({
            data: {
                type: "projects",
                attributes: {
                    provider: "pharbers",
                    name: "AlexProject1",
                    type: "paas",
                },
                relationships: {
                    owner: {
                        data: {
                            type: "resources",
                            id: "VSq8W2iKoU3pY0OG"
                        }
                    }
                }
            }
        })
        const event = template()
        event.path = "/phcreatereproject/projects"
        event.httpMethod = "POST"
        event.pathParameters = {
            type: "projects"
        }
        event.body = body

        const response = await app.lambdaHandler(event, undefined)
        console.info(response)
    })

    test("Handler Test", () => {
        const handler = new OptEfsHandler()
        handler.create("lGiiLUcHPrWb7xpJw_I_")
    })
})
