import BaseModel from "../models/BaseModel"
import Register from "./Register"

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
        this.typeAnalyzerMap.set(model.name, model)
    }

    getData(name: string): BaseModel {
        return this.typeAnalyzerMap.get(name)
    }

    size(): number {
        return this.typeAnalyzerMap.size
    }
}