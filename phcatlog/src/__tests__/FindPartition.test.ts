import * as fs from "fs"

const FindFilterPartitionSuccess = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/catlog/catlog_find_partition.json", "utf8"))
})

test("Find Partitions For DataBaseName AND Table Success", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new FindFilterPartitionSuccess(), undefined)
    console.info(result)
}, 1000 * 60 * 10)
