"use strict"

import ServerConf from "../../config/ServerConf"
import { Store, IStore } from "./Store"
import RedisAdapter from "fortune-redis"
import fortune from "fortune"

export interface IRedisStore extends IStore {
    setExpire(key: string, value: any, expire: number): Promise<any>
}

export default class RedisStore extends Store implements IRedisStore {
    constructor(conf: ServerConf) {
        super()
        if (conf.redis) {
            const record = new (this.getRecord(conf.redis.entry))()
            const option = Object.assign(
                {
                    adapter: [RedisAdapter, { url: conf.redis.getUrl() }],
                },
                record.operations,
            )
            this.store = fortune(record.model, option)

        } else {
            throw new Error("Server Config Redis Is Null")
        }
    }

    async setExpire(key: string, value: any, expire: number): Promise<any> {
        if (!this.store) {
            throw new Error("Redis Store未实例化，请检查配置")
        }
       return await this.store.adapter.redis.set(key, value, "EX", expire)
    }

    async create(type: string, records: any, include: any, meta: any): Promise<any> {
        return await this.store.create(type, records, include, meta)
    }
    async find(type: string, ids: any, options: any, include: any, meta: any): Promise<any> {
        return await this.store.find(type, ids, options, include, meta)
    }

    async update(type: string, updates: any, include: any, meta: any): Promise<any> {
        return await this.store.update(type, updates, include, meta)
    }

    async delete(type: string, ids: any, include: any, meta: any): Promise<any> {
        return await this.store.delete(type, ids, include, meta)
    }

    async open() {
        return await this.store.connect()
    }

    async close() {
        return await this.store.disconnect()
    }
}
