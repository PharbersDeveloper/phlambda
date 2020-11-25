import {Main, Logger, ServerConfig, PostgresConfig, RedisConfig} from "../index"
import * as fs from "fs"
import ConfRegistered from "../config/ConfRegistered"

test("Test DB Connect", async () => {
    const pg = new PostgresConfig(
        "entry",
        "postgres",
        "faiz",
        "127.0.0.1",
        5432,
        "phtest"
    )
    ConfRegistered.getInstance.registered(pg)
    const event = JSON.parse(fs.readFileSync("../events/event_entry_find.json", "utf8"))
    const a = [1,2,3,4]
    for (const i of a) {
        const result = await Main(event)
        expect(result.statusCode).toBe(200)
        Logger.info(String(result["output"][1]))
    }
})

