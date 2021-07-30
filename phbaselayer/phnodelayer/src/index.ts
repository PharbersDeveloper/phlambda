import AWSRequest from "./common/request/AWSRequest"
import BuildMaker from "./build/BuildMaker"
import Config from "./common/config/Config"
import DBConfig from "./common/config/DBConfig"
import IStore from "./common/store/IStore"
import JSONAPIDelegate from "./delegate/JSONAPIDelegate"
import PhLogger from "./common/logger/phLogger"
import { StoreEnum } from "./common/enum/StoreEnum"
import StoreRegister from "./common/factory/StoreRegister"

const JSONAPI = async (jsonApiDB: StoreEnum, event: any) => {
    let result: any = null
    let delegate: any = null
    try {
        delegate = new JSONAPIDelegate()
        if (delegate.isFirstInit && event !== null && event !== undefined) {
            await delegate.prepare(jsonApiDB)
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

const ServerRegisterConfig = (configs: Config[]) => {
    // tslint:disable-next-line:no-unused-expression
    new BuildMaker(configs)
}

export {
    AWSRequest,
    PhLogger as Logger,
    DBConfig,
    IStore,
    JSONAPI,
    StoreEnum,
    StoreRegister as Register,
    ServerRegisterConfig,
}


