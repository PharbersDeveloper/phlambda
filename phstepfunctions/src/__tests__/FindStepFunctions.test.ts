
import * as fs from "fs"

const FindStepFunctionsPage = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/stepfunction/stepfunction_find_page.json", "utf8"))
})

test("Find Step Functions Page", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new FindStepFunctionsPage(), undefined)
    console.info(result)
})

