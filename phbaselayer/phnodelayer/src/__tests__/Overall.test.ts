import { Logger, DBConfig, JSONAPI, StoreEnum, Register, IStore, ServerRegisterConfig } from "../index"
import * as fs from "fs"
import * as util from "util"


const findEvent = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../../events/nodelayer/event_entry_find.json", "utf8"))
})

const updateEvent = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../../events/nodelayer/event_entry_update.json", "utf8"))

})

const deleteEvent = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../../events/nodelayer/event_entry_delete.json", "utf8"))

})

const registerConfigs = jest.fn(() => {
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
        entity: "redis",
        database: "0",
        user: "",
        password: "",
        host: "127.0.0.1",
        port: 6379,
        poolMax: 1
    })

    return [jsonapiDBConfig, redisDBConfig]
})

const throwError = jest.fn( () => {
    const jsonapiDBConfig = new DBConfig({
        name: StoreEnum.POSTGRES,
        entity: "entry",
        database: "phentry",
        user: "pharbers",
        password: "Abcde196125",
        host: "127.0.0.1",
        port: 5433,
        poolMax: 1
    })
    return [jsonapiDBConfig]
})

test("JSONAPI Find", async () => {
    const configs = new registerConfigs()
    ServerRegisterConfig(configs)
    const result = await JSONAPI(StoreEnum.POSTGRES, new findEvent())
    expect(result.hasOwnProperty("outputData")).toBe(true)
    expect(typeof result.outputData[0].data).toEqual("string")
    expect(typeof result.outputData[1].data).toEqual("object")
    expect(JSON.parse(result.outputData[1].data.toString()).hasOwnProperty("jsonapi")).toBe(true)
    expect(JSON.parse(result.outputData[1].data.toString()).hasOwnProperty("meta")).toBe(true)
    expect(JSON.parse(result.outputData[1].data.toString()).hasOwnProperty("links")).toBe(true)
    expect(JSON.parse(result.outputData[1].data.toString()).hasOwnProperty("data")).toBe(true)

}, 1000 * 60 * 2)

test("JSONAPI Update", async () => {
    const configs = new registerConfigs()
    ServerRegisterConfig(configs)
    const result = await JSONAPI(StoreEnum.POSTGRES, new updateEvent())
    expect(result.hasOwnProperty("outputData")).toBe(true)
    expect(typeof result.outputData[0].data).toEqual("string")
    expect(typeof result.outputData[1].data).toEqual("object")
    expect(JSON.parse(result.outputData[1].data.toString()).hasOwnProperty("jsonapi")).toBe(true)
    expect(JSON.parse(result.outputData[1].data.toString()).hasOwnProperty("links")).toBe(true)
    expect(JSON.parse(result.outputData[1].data.toString()).hasOwnProperty("data")).toBe(true)
    expect(JSON.parse(result.outputData[1].data.toString()).data.attributes.name).toEqual("change name")
})

test("JSONAPI Delete", async () => {
    const configs = new registerConfigs()
    ServerRegisterConfig(configs)
    const result = await JSONAPI(StoreEnum.POSTGRES, new deleteEvent())
    expect(result.outputSize).toBeGreaterThan(0)
})

test("set value to Redis", async () => {
    const configs = new registerConfigs()
    ServerRegisterConfig(configs)
    const redisStore = (Register.getInstance.getData(StoreEnum.REDIS) as IStore)
    redisStore.open()
    const store = redisStore.getStore()
    const data = {
        name: "Alex",
        age: 27
    }
    const createResult = await redisStore.create("user", data)
    store.adapter.redis.set(
        `user:${createResult.payload.records[0].id}`,
        JSON.stringify(createResult.payload.records[0]),
        "EX",
        60,
    )
    const result = await redisStore.find("user", null)
    expect(result.payload.records[0].name).toEqual("Alex")
    expect(result.payload.records[0].age).toBe(27)
    redisStore.close()
})

test("throw error", async () => {
    try {
        const configs = new throwError()
        ServerRegisterConfig(configs)
        await JSONAPI(StoreEnum.POSTGRES, new findEvent())
    } catch(error) {
        expect(util.types.isNativeError(error)).toBe(true)
    }

})

test("logger print", () => {
    Logger.info("I'm Info Message")
    Logger.warn("I'm Warning Message")
    Logger.error("I'm Error Message")
    Logger.debug("I'm Debug Message")
})

