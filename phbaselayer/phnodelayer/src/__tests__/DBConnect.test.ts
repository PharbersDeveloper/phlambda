// import {
//     ConfigRegistered,
//     JsonApiMain,
//     Logger,
//     PostgresConfig,
//     RedisConfig,
//     MongoConfig,
//     SF,
//     Store
// } from "../index"
// import * as fs from "fs"
// import RedisStore from "../strategies/store/RedisStore"
//
// test("Postgres DB Connect", async () => {
//     const pg = new PostgresConfig(
//         "entry",
//         "pharbers",
//         "Abcde196125",
//         "127.0.0.1",
//         5432,
//         "phtest"
//     )
//     ConfigRegistered.getInstance.registered(pg)
//     const event = JSON.parse(fs.readFileSync("../../events/event_entry_find.json", "utf8"))
//     const db = SF.getInstance.get(Store.Postgres)
//     const list = Array.from({ length: 1 }, (v, k) => k )
//     await db.open()
//     for (const i of list) {
//         const result = await JsonApiMain({event, db})
//         expect(result.statusCode).toBe(201)
//         // Logger.info(String(result["output"][1]))
//     }
//     // const result2 = await db.find("asset", null, { match: { name: "chc" } })
//     // Logger.info(result2.payload.records.length)
//     await db.close()
// }, 1000 * 60 * 100)
//
// test("Redis DB Connect", async () => {
//     const rd = new RedisConfig(
//         "TestRedis",
//         "",
//         "",
//         "127.0.0.1",
//         6379,
//         "0"
//     )
//     ConfigRegistered.getInstance.registered(rd)
//     const event = JSON.parse(fs.readFileSync("../../events/event_entry_find.json", "utf8"))
//     const db = SF.getInstance.get(Store.Redis)
//     await db.open()
//     if (db instanceof RedisStore) {
//         await db.setExpire("test", "123", 100000)
//     }
//     await db.close()
// }, 1000 * 60 * 100)
//
// test("Mongo DB Connect", async () => {
//     const mo = new MongoConfig(
//         "mongodb",
//         "entry",
//         "",
//         "",
//         "localhost",
//         27017,
//         "pharbers-tm"
//     )
//
//     ConfigRegistered.getInstance.registered(mo)
//     const event = JSON.parse(fs.readFileSync("../../events/ntm/event_ntm_upload.json", "utf8"))
//     const db = SF.getInstance.get(Store.Mongo)
//     const list = Array.from({ length: 1 }, (v, k) => k )
//     for (const i of list) {
//         await db.open()
//         // await db.find("test", "60505e4b81ef2c5db38b468a")
//         const result = await JsonApiMain({event, db})
//         await db.close()
//         // expect(result.statusCode).toBe(201)
//         Logger.info(String(result["output"][1]))
//     }
//
// }, 1000 * 60 * 100)
test("init", async () => {

})
