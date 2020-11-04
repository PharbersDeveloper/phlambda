"use strict"

import { StoreEnum } from "../../common/StoreEnum"
import DBFactory from "../../factory/DBFactory"

// TODO 暂时先做一个，调试成功后吧所有存储操对接口变成
export interface IStore {
    // store: any
    open(): void
    close(): void
}

export interface IRedisStore extends IStore {
    setExpire(key: string, value: any, expire: number): any
}

export default class RedisStore implements IRedisStore {
    private static instance: RedisStore = null
    private readonly store: any

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
        if (this.store === undefined) {
            throw new Error("Redis Store未实例化，请检查配置")
        }
       return await this.store.adapter.redis.set(key, value, "EX", expire)
    }

    public async create(type: string, records: any, include: any, meta: any) {
        return await this.store.create(type, records, include, meta)
    }
    public async find(type: string, ids: any, options: any, include: any, meta: any) {
        return await this.store.find(type, ids, options, include, meta)
    }

    public async update(type: string, updates: any, include: any, meta: any) {
        return await this.store.update(type, updates, include, meta)
    }

    public async delete(type: string, ids: any, include: any, meta: any) {
        return await this.store.delete(type, ids, include, meta)
    }

    public async open() {
        await this.store.connect()
    }

    public async close() {
        await this.store.disconnect()
    }
}
