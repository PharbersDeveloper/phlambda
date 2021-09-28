import * as fs from "fs"
import { Logger } from "phnodelayer"

const UpdateProjectFunction = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/max/event_update_project.json", "utf8"))
})

describe("Update Test", () => {
    test("Update Project", async () => {
        const app = require("../../app.js")
        const result = await app.lambdaHandler(new UpdateProjectFunction(), undefined)
        Logger.info(result)
        expect(result.statusCode).toBe(200)
    }, 1000 * 60 * 10)
})
