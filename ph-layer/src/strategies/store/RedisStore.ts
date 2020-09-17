"use strict"

import { StoreEnum } from "../../common/StoreEnum"
import DBFactory from "../../dbFactory/DBFactory"

// TODO 暂时先做一个，调试成功后吧所有存储操对接口变成
export interface IStore {
    // store: any
    open()
    close()
}

export interface IRedisStore extends IStore {
    setExpire(key: string, value: any, expire: number)
}

export default class RedisStore implements IRedisStore {

    private static instance: RedisStore = null
    private readonly store

    constructor() {
        this.store = DBFactory.getInstance.getStore(StoreEnum.Redis)
    }

    public static get getInstance() {
        if (RedisStore.instance == null) {
            RedisStore.instance = new RedisStore()
        }
        return RedisStore.instance
    }

    public async setExpire(key: string, value: any, expire: number) {
        if (this.store === undefined) {throw new Error("Redis Store未实例化，请检查配置")}
        await this.store.adapter.redis.set(key, value, "EX", expire)
    }

     public async open() {
        await this.store.connect()
    }

    public async close() {
        await this.store.disconnect()
    }

}
