import DBConfig from "../common/config/DBConfig"
import ConfigRegister from "../common/factory/ConfigRegister"
import StoreRegister from "../common/factory/StoreRegister"
import {StoreEnum} from "../common/enum/StoreEnum"
import PhLogger from "../common/logger/phLogger"
import PhStore from "../common/store/PhStore"
import IStore from "../common/store/IStore"

const createDBConfig = jest.fn(() => {
    return new DBConfig({
        name: StoreEnum.POSTGRES,
        entity: "entry",
        database: "phentry",
        user: "pharbers",
        password: "Abcde196125",
        host: "127.0.0.1",
        port: 5432,
        poolMax: 2
    })
})

const registerConfig = jest.fn(() => {
    const dbConfig = new createDBConfig()
    const config = ConfigRegister.getInstance
    config.register(dbConfig)
    return dbConfig
})

const registerStore = jest.fn(() => {
    const rg = new registerConfig()
    const store = StoreRegister.getInstance
    store.register(new PhStore(rg.name))
    return store
})

test("register store to StoreRegister", () => {
    const store = new registerStore()
    PhLogger.info("register data size => ", store.size())
    expect(store.size()).toBeGreaterThan(0)
})

test("get store registration center data", () => {
    const store = new registerStore()
    const storeData = store.getData(StoreEnum.POSTGRES)
    expect(storeData.name).toEqual(StoreEnum.POSTGRES)
})

test("find asset data count", async () => {
    const store = new registerStore()
    const storeData = store.getData(StoreEnum.POSTGRES) as PhStore
    await storeData.open()
    const result = await storeData.find("asset", null)
    await storeData.close()
    expect(result.payload.records.length).toBeGreaterThan(0)
}, 1000 * 60)