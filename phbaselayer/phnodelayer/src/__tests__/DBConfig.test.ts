import * as fs from "fs"
import DBConfig from "../common/config/DBConfig"
import {StoreEnum} from "../common/enum/StoreEnum"
import PhLogger from "../common/logger/PhLogger"

const createDBConfig = jest.fn(() => {
    return new DBConfig({
        name: StoreEnum.POSTGRES,
        entity: "entry",
        database: "phentry",
        user: "admin",
        password: "Abcde196125",
        host: "127.0.0.1",
        port: 0,
        poolMax: 1000
    })
})

test("Create DBConfig", () => {
    const config = new createDBConfig()
    expect(config.getConf().name).toEqual(StoreEnum.POSTGRES)
})

test("DBConfig toString Func", () => {
    const config = new createDBConfig()
    expect(config.toString()).toEqual("")
})

test("DBConfig toStructure Func", () => {
    const config = new createDBConfig()
    expect(config.toStructure().database).toEqual("phentry")
    expect(config.toStructure().user).toEqual("admin")
    expect(config.toStructure().password).toEqual("Abcde196125")
    expect(config.toStructure().host).toEqual("127.0.0.1")
    expect(config.toStructure().ssl).toBe(false)
    expect(config.toStructure().port).toBe(0)
    expect(config.toStructure().max).toBe(1000)
    expect(config.toStructure().idleTimeoutMillis).toBe(1000)
    expect(config.toStructure().connectionTimeoutMillis).toBe(1000)
})
