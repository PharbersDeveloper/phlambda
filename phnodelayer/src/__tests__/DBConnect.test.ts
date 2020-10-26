import { Main } from "../index"
import * as fs from "fs"

test("Test DB Connect", async () => {
    jest.setTimeout(1000 * 60 * 2)
    async function sleep(ms: number) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve('')
            }, ms)
        })
    }

    const event = JSON.parse(fs.readFileSync("../events/event_success_find_one.json", 'utf8'))
    await Main(event)

    await sleep(1000 * 60)
})
