import AWSRequest from "./common/request/AWSRequest"
import Config from "./common/config/Config"
import DBConfig from "./common/config/DBConfig"
import IStore from "./common/store/IStore"
import JSONAPIDelegate from "./delegate/JSONAPIDelegate"
import PhLogger from "./common/logger/phLogger"
import { StoreEnum } from "./common/enum/StoreEnum"
import StoreRegister from "./common/factory/StoreRegister"

const JSONAPI = async (jsonApiDB: StoreEnum, configs: Config[], event: any) => {
    let result = null
    let delegate = null
    try {
        delegate = new JSONAPIDelegate()
        if (delegate.isFirstInit && event !== null && event !== undefined) {
            await delegate.prepare(jsonApiDB, configs)
            result = await delegate.exec(event)
        }
        return result
    } catch (error) {
        throw error
    } finally {
        if (delegate !== null) {
            delegate.isFirstInit = true
        }
    }
}

export {
    PhLogger as Logger,
    StoreRegister as Register,
    DBConfig,
    IStore,
    AWSRequest,
    JSONAPI,
    StoreEnum
}


