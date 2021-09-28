import BaseModel from "../models/BaseModel"
import Register from "./Register"
import PhLogger from "../logger/phLogger"
import GetCSInstance from "../../util/GetCSInstance"

export default class ConfigRegister extends Register {

    private static instance: ConfigRegister = null
    private constructor() {
        super()
    }

    static get getInstance() {
        if (ConfigRegister.instance === null) {
            ConfigRegister.instance = new ConfigRegister()
        }
        return ConfigRegister.instance
    }


    register(model: BaseModel): void {
        PhLogger.info(`${model.name} Config Registering`)
        this.typeAnalyzerMap.set(model.name, model)
    }

    getData(name: string): BaseModel {
        if (this.typeAnalyzerMap.size === 0) {
            return GetCSInstance.getInstance.getConfig(name)
        }
        return this.typeAnalyzerMap.get(name)
    }

    size(): number {
        return this.typeAnalyzerMap.size
    }


}
