import ConfigRegister from "../common/factory/ConfigRegister"
import StoreRegister from "../common/factory/StoreRegister"
import PhStore from "../common/store/PhStore"
import Config from "../common/config/Config"

export default class BuildMaker {
    constructor(configs?: Config[]) {
        configs.forEach((item: Config) => {
            ConfigRegister.getInstance.register(item)
            StoreRegister.getInstance.register(new PhStore(item.name))
        })
    }
}
