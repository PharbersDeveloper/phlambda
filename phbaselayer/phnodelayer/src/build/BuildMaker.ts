
import PhLogger from "../common/logger/phLogger"
import ConfigRegister from "../common/factory/ConfigRegister"
import StoreRegister from "../common/factory/StoreRegister"
import PhStore from "../common/store/PhStore"
import Config from "../common/config/Config"

export class BuildMaker {


    constructor(entity: string, configs: Config[]) {
        const configRegister = ConfigRegister.getInstance
        const storeRegister = StoreRegister.getInstance
        configs.forEach((item) => {
            PhLogger.info(item.name)
            configRegister.register(item)
        })
        
        const store = new PhStore(entity)
        storeRegister.register(store)
    }

}
