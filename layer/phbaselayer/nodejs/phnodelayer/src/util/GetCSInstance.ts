import ConfigRegister from "../common/factory/ConfigRegister"
import StoreRegister from "../common/factory/StoreRegister"
import Register from "../common/factory/Register"
import DBConfig from "../common/config/DBConfig"
import PhStore from "../common/store/PhStore"

export default class GetCSInstance {
    private static instance: GetCSInstance = null
    private readonly _config: Register
    private readonly _store: Register
    private readonly _evn: any

    private constructor() {
        const configSize = ConfigRegister.getInstance.size()
        if (configSize > 0) {
            this._config = ConfigRegister.getInstance
            this._store = StoreRegister.getInstance
        }
        this._evn = JSON.parse(process.env.configs)
    }

    static get getInstance() {
        if (GetCSInstance.instance === null) {
            GetCSInstance.instance = new GetCSInstance()
        }
        return GetCSInstance.instance
    }

    getConfig(key: string) {
        if (this._config) {
            return this._config.getData(key)
        } else {
            const findConfig = this._evn.find((item: any) => item.name === key)
            return new DBConfig(findConfig)
        }
    }

    getStore(key: string) {
        if (this._store) {
            return this._store.getData(key)
        } else {
            return new PhStore(key)
        }
    }
}
