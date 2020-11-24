import {Main, Logger, ServerConfig, PostgresConfig, RedisConfig} from "../index"
import * as fs from "fs"

// test("Test DB Connect", async () => {
//
// })

test("并发测试1", async () => {
    const sc = new ServerConfig("layer test", {
        pg: new PostgresConfig(
            "entry",
            "postgres",
            "faiz",
            "127.0.0.1",
            5432,
            "phtest"
        ),
        redis: new RedisConfig(
            "TestRedis",
            "",
            "",
            "127.0.0.1",
            6379,
            "0"
        )
    })

    const event = JSON.parse(fs.readFileSync("../events/event_entry_find.json", "utf8"))
    const a = [1,2,3,4]
    for (const i of a) {
        const result = await Main(event, sc)
        expect(result.statusCode).toBe(200)
    }
})

test("并发测试2", async () => {
    const sc = new ServerConfig("layer test", {
        pg: new PostgresConfig(
            "entry",
            "postgres",
            "faiz",
            "127.0.0.1",
            5432,
            "phtest"
        ),
        redis: new RedisConfig(
            "TestRedis",
            "",
            "",
            "127.0.0.1",
            6379,
            "0"
        )
    })

    const event = JSON.parse(fs.readFileSync("../events/event_entry_find.json", "utf8"))
    const a = [1]
    for (const i of a) {
        const result = await Main(event, sc)
        expect(result.statusCode).toBe(200)
    }
})

test("并发测试3", async () => {
    const sc = new ServerConfig("layer test", {
        pg: new PostgresConfig(
            "entry",
            "postgres",
            "faiz",
            "127.0.0.1",
            5432,
            "phtest"
        ),
        redis: new RedisConfig(
            "TestRedis",
            "",
            "",
            "127.0.0.1",
            6379,
            "0"
        )
    })

    const event = JSON.parse(fs.readFileSync("../events/event_entry_find.json", "utf8"))
    const a = [1,2,3,4,5,6,7,8]
    for (const i of a) {
        const result = await Main(event, sc)
        expect(result.statusCode).toBe(200)
    }
})


test("并发测试4", async () => {
    const sc = new ServerConfig("layer test", {
        pg: new PostgresConfig(
            "entry",
            "postgres",
            "faiz",
            "127.0.0.1",
            5432,
            "phtest"
        ),
        redis: new RedisConfig(
            "TestRedis",
            "",
            "",
            "127.0.0.1",
            6379,
            "0"
        )
    })

    const event = JSON.parse(fs.readFileSync("../events/event_entry_find.json", "utf8"))
    const a = [1,2,3]
    for (const i of a) {
        const result = await Main(event, sc)
        expect(result.statusCode).toBe(200)
    }
})

test("并发测试5", async () => {
    const sc = new ServerConfig("layer test", {
        pg: new PostgresConfig(
            "entry",
            "postgres",
            "faiz",
            "127.0.0.1",
            5432,
            "phtest"
        ),
        redis: new RedisConfig(
            "TestRedis",
            "",
            "",
            "127.0.0.1",
            6379,
            "0"
        )
    })

    const event = JSON.parse(fs.readFileSync("../events/event_entry_find.json", "utf8"))
    const a = [1,2,3,4,5]
    for (const i of a) {
        const result = await Main(event, sc)
        expect(result.statusCode).toBe(200)
    }
})
