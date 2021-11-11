import BaseModel from "../models/BaseModel"
import Register from "./Register"
import GetCSInstance from "../../util/GetCSInstance"
import PhLogger from "../logger/phLogger"

export default class StoreRegister extends Register {

    private static instance: StoreRegister = null
    private constructor() {
        super()
    }

    static get getInstance() {
        if (StoreRegister.instance === null) {
            StoreRegister.instance = new StoreRegister()
        }
        return StoreRegister.instance
    }

    register(model: BaseModel): void {
        if (this.typeAnalyzerMap.has(model.name)) {
            PhLogger.info(`${model.name} Config Already Exists`)
        } else {
            this.typeAnalyzerMap.set(model.name, model)
        }
    }

    getData(name: string): BaseModel {
        if (this.typeAnalyzerMap.size === 0) {
            return GetCSInstance.getInstance.getStore(name)
        }
        return this.typeAnalyzerMap.get(name)
    }

    size(): number {
        return this.typeAnalyzerMap.size
    }
}
