"use strict"

import { Store, IStore } from "./Store"
import RedisAdapter from "fortune-redis"
import fortune from "fortune"
import ConfRegistered from "../../config/ConfRegistered"
import {StoreEnum} from "../../common/StoreEnum"

export interface IRedisStore extends IStore {
    setExpire(key: string, value: any, expire: number): Promise<any>
}

export default class RedisStore extends Store implements IRedisStore {
    constructor() {
        super()
        this.name = StoreEnum.Redis
        const conf = ConfRegistered.getInstance.getConf("RedisConf")
        if (!conf) { throw new Error("RedisConf Is Null")}
        const record = new (this.getRecord(conf.entry))()
        const option = Object.assign(
            {adapter: [RedisAdapter, {url: conf.getUrl()}]},
            record.operations,
        )
        this.store = fortune(record.model, option)
    }

    async setExpire(key: string, value: any, expire: number): Promise<any> {
        if (!this.store) {
            throw new Error("Redis Store未实例化，请检查配置")
        }
       return await this.store.adapter.redis.set(key, value, "EX", expire)
    }
}
