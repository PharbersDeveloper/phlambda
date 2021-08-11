import SnowflakeID from "../utils/SnowflakeID"

describe("Utils Test", () => {
    test("Snowflakes Test", () => {
        console.time("id")
        const tempIds = []
        const idGenerate = new SnowflakeID()
        for (let i = 0; i < 50000000; i++) {
            tempIds.push(idGenerate.nextId())
        }
        console.info(tempIds.length)
        console.timeEnd("id")

        for (let i = 1; i < tempIds.length - 2; i++) {
            if (tempIds[i] >= tempIds[i + 1]) {
                console.info("Fuck")
            }
        }
    })
})
