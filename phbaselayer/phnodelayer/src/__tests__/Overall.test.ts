import { Logger, DBConfig, JSONAPI, StoreEnum } from "../index"
import * as fs from "fs"



const event = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../../events/nodelayer/event_entry_find.json", "utf8"))
})


test("JSONAPI Simulation Of The Request", async () => {
    const jsonapiDBConfig = new DBConfig({
        name: StoreEnum.POSTGRES,
        entity: "entry",
        database: "phentry",
        user: "pharbers",
        password: "Abcde196125",
        host: "127.0.0.1",
        port: 5432,
        poolMax: 1
    })

    const redisDBConfig = new DBConfig({
        name: StoreEnum.REDIS,
        entity: "token",
        database: "0",
        user: "",
        password: "",
        host: "127.0.0.1",
        port: 6479,
        poolMax: 1
    })

    const configs = [jsonapiDBConfig]
    const result = await JSONAPI(StoreEnum.POSTGRES, configs, new event())
    Logger.info(result)

}, 1000 * 60 * 2)

