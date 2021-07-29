
import ConfigRegister from "../common/factory/ConfigRegister"
import StoreRegister from "../common/factory/StoreRegister"
import PhStore from "../common/store/PhStore"
import Config from "../common/config/Config"
import {StoreEnum} from "../common/enum/StoreEnum"

export default class BuildMaker {
    constructor(configs: Config[]) {
        const configRegister = ConfigRegister.getInstance
        const storeRegister = StoreRegister.getInstance
        configs.forEach((item: Config) => {
            configRegister.register(item)
            storeRegister.register(new PhStore(item.name))
        })
    }

    getStore(jsonApiDB: StoreEnum): PhStore {
        return (StoreRegister.getInstance.getData(jsonApiDB) as PhStore)
    }

}
