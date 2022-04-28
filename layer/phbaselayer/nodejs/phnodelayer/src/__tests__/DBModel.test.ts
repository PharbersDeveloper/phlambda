import * as fs from "fs"
import DBModel from "../common/models/DBModel"
import {StoreEnum} from "../common/enum/StoreEnum"
import PhLogger from "../common/logger/phLogger"


const createDBModel = jest.fn(() => {
    return new DBModel({
        name: StoreEnum.POSTGRES,
        database: "phentry",
        user: "admin",
        password: "Abcde196125",
        host: "127.0.0.1",
        port: 5555,
        max: 1000,
    })
})

test("Create DBModel", () => {
    const model = new createDBModel()
    expect(model.name).toEqual(StoreEnum.POSTGRES)
})

test("DBModel toString Func", () => {
    const model = new createDBModel()
    expect(model.toString()).toEqual("")
})

test("DBModel toStructure Func", () => {
    const model = new createDBModel()
    expect(model.toStructure().database).toEqual("phentry")
    expect(model.toStructure().user).toEqual("admin")
    expect(model.toStructure().password).toEqual("Abcde196125")
    expect(model.toStructure().host).toEqual("127.0.0.1")
    expect(model.toStructure().ssl).toBe(false)
    expect(model.toStructure().port).toBe(5555)
    expect(model.toStructure().max).toBe(1000)
    expect(model.toStructure().idleTimeoutMillis).toBe(1000)
    expect(model.toStructure().connectionTimeoutMillis).toBe(1000)
})

