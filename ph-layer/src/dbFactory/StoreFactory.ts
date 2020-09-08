"use strict"

import { StoreEnum } from "../common/StoreEnum"
import { MongoDBFactory } from "./MongoDBFactory"
import { MysqlFactory } from "./MysqlFactory"
import { PostgresFactory } from "./PostgresFactory"

export interface IStoreInterface {
    getStore(): any
}

export class StoreFactory {
    // tslint:disable-next-line:variable-name
    private static _instance: StoreFactory = null
    private closeTypeAnalyzerMapping: Map<StoreEnum, IStoreInterface> = new Map()
    constructor() {
        this.closeTypeAnalyzerMapping.set(StoreEnum.Postgres, new PostgresFactory())
        this.closeTypeAnalyzerMapping.set(StoreEnum.MongoDB, new MongoDBFactory())
        this.closeTypeAnalyzerMapping.set(StoreEnum.Mysql, new MysqlFactory())
    }

    public static get instance() {
        if (this._instance == null) {
            this._instance = new StoreFactory()
        }
        return this._instance
    }

    public getStore(type: StoreEnum): IStoreInterface {
        if (this.closeTypeAnalyzerMapping.has(type)) {
            return this.closeTypeAnalyzerMapping.get(type).getStore()
        } else {
            throw new Error("our factory don\'t have this type")
        }
    }

}
