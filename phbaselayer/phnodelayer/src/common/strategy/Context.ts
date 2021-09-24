import IStrategy from "./IStrategy"
import DBModel from "../models/DBModel"
import { Strategy } from "./Strategy"

export default class Context {
    private readonly _strategy: IStrategy
    private readonly _config: DBModel

    constructor(config: DBModel) {
        this._config = config
        this._strategy = new (Strategy as any)[`${config.name}Strategy`]() as IStrategy
    }

    doChoose(): any {
        return this._strategy.choose(this._config)
    }
}
