
import DBConfig from "../common/config/DBConfig"
import ConfigRegister from "../common/factory/ConfigRegister"
import {StoreEnum} from "../common/enum/StoreEnum"
import PhLogger from "../common/logger/phLogger"

const createDBConfig = jest.fn(() => {
    return new DBConfig({
        name: StoreEnum.POSTGRES,
        entity: "entry",
        database: "phentry",
        user: "admin",
        password: "123",
        host: "127.0.0.1",
        port: 5555,
        poolMax: 1
    })
})

const register = jest.fn(() => {
    const dbConfig = new createDBConfig()
    const config = ConfigRegister.getInstance
    config.register(dbConfig)
    return true
})

test("register database config use ConfigRegister", () => {
    const rg = new register()
    const config = ConfigRegister.getInstance
    PhLogger.info("register data size => ", config.size())
    expect(config.size()).toBeGreaterThan(0)
})

test("get registration center data", () => {
    const rg = new register()
    const config = ConfigRegister.getInstance
    const configData = config.getData(StoreEnum.POSTGRES)
    const structure = configData.toStructure()
    expect(structure.name).toEqual(StoreEnum.POSTGRES)
    expect(structure.database).toEqual("phentry")
})
