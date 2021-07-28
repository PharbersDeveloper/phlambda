import BaseModel from "../models/BaseModel"
import Register from "./Register"

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
        this.typeAnalyzerMap.set(model.name, model)
    }

    getData(name: string): BaseModel {
        return this.typeAnalyzerMap.get(name)
    }

    size(): number {
        return this.typeAnalyzerMap.size
    }


}