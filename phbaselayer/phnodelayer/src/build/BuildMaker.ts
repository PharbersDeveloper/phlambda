import ConfigRegister from "../common/factory/ConfigRegister"
import StoreRegister from "../common/factory/StoreRegister"
import PhStore from "../common/store/PhStore"
import Config from "../common/config/Config"

export default class BuildMaker {
    constructor(configs: Config[]) {
        const configRegister = ConfigRegister.getInstance
        const storeRegister = StoreRegister.getInstance
        configs.forEach((item: Config) => {
            configRegister.register(item)
            storeRegister.register(new PhStore(item.name))
        })
    }
}
