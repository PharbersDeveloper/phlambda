import BaseModel from "../models/BaseModel"

export default abstract class Register {
    protected typeAnalyzerMap: Map<string, BaseModel> = new Map()

    abstract register(model: BaseModel): void

    abstract getData(name: string): BaseModel

    abstract size(): number
}