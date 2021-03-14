import {JsonApiMain, Logger, PostgresConfig, RedisConfig, SF, Store} from "../index"
import * as fs from "fs"
import ConfRegistered from "../config/ConfRegistered"

test("Test DB Connect", async () => {
    const pg = new PostgresConfig(
        "entry",
        "pharbers",
        "Abcde196125",
        "127.0.0.1",
        5432,
        "phtest"
    )
    ConfRegistered.getInstance.registered(pg)
    const event = JSON.parse(fs.readFileSync("../../events/event_entry_find.json", "utf8"))
    const db = SF.getInstance.get(Store.Postgres)
    const list = Array.from({ length: 1 }, (v, k) => k )
    await db.open()
    for (const i of list) {
        const result = await JsonApiMain({event, db})
        expect(result.statusCode).toBe(201)
        // Logger.info(String(result["output"][1]))
    }
    // const result2 = await db.find("asset", null, { match: { name: "chc" } })
    // Logger.info(result2.payload.records.length)
    await db.close()
}, 1000 * 60 * 100)

