import PostgresAdapter from "fortune-postgres"
import RedisAdapter from "fortune-redis"
import MongoAdapter from "fortune-mongodb"
import ConfigRegister from "../factory/ConfigRegister"
import {StoreEnum} from "../enum/StoreEnum"
import IStore from "./IStore"
import * as fs from "fs"
import fortune from "fortune"
import DBConfig from "../config/DBConfig"


export default class PhStore implements IStore {
    name: string
    private readonly store: any
    private readonly adapter: Map<string, any> = new Map<string, any>([
        [StoreEnum.POSTGRES, PostgresAdapter],
        [StoreEnum.REDIS, RedisAdapter],
        [StoreEnum.MONGO, MongoAdapter],
    ])

    // 处理Entity与store实例,其他的都不干
    constructor(key: string) {
        this.name = key
        const config = ConfigRegister.getInstance.getData(key) as DBConfig
        const record = new (this.getRecord(config.entity))()
        const structure = config.toStructure()
        const option = Object.assign(
            { adapter: [this.adapter.get(key), structure] },
            record.operations
        )
        this.store = fortune(record.model, option)
    }

    toString(): string {
        throw new Error("toString Method not implemented.")
    }

    toStructure() {
        throw new Error("toStructure Method not implemented.")
    }

    private getRecord(entity: string): any {
        const base = process.cwd()
        try {
            fs.statSync(`${base}/dist/models`)
            return require(`${base}/dist/models/${entity}.js`).default
        } catch (error) {
            return require(`${base}/lib/models/${entity}.js`).default
        }
    }

    async open() {
        await this.store.connect()
    }

    async close() {
        await this.store.disconnect()
    }

    async create(type: string, records: any, include?: any, meta?: any): Promise<any> {
        return await this.store.create(type, records, include, meta)
    }

    async delete(type: string, ids: string | string[], include?: any, meta?: any): Promise<any> {
        return await this.store.delete(type, ids, include, meta)
    }

    async find(type: string, ids?: string | string[], options?: any, include?: any, meta?: any): Promise<any> {
        return await this.store.find(type, ids, options, include, meta)
    }

    async update(type: string, updates: any, include?: any, meta?: any): Promise<any> {
        return await this.store.update(type, updates, include, meta)
    }

    getStore(): any {
        return this.store
    }

    isConnect(): boolean {
        return !(this.store.connectionStatus === 0)
    }
}
