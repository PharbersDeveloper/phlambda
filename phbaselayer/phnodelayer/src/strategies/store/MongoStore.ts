"use strict"

import { Store } from "./Store"
import MongoAdapter from "fortune-mongodb"
import fortune from "fortune"
import ConfRegistered from "../../config/ConfRegistered"
import {StoreEnum} from "../../common/StoreEnum"

export default class MongoStore extends Store {
    constructor() {
        super()

        this.name = StoreEnum.Mongo
        const conf = ConfRegistered.getInstance.getConf("MongoConf")
        if (!conf) { throw new Error("MongoConf Is Null")}
        const record = new (this.getRecord(conf.entry))()
        const option = Object.assign(
            { adapter: [ MongoAdapter, { url: conf.getUrl() } ] },
            record.operations,
        )

        this.store = fortune(record.model, option)
        // if (conf.postgres) {
        //     const record = new (this.getRecord(conf.postgres.entry))()
        //     const option = Object.assign(
        //         {
        //             adapter: [PostgresAdapter, { connection: conf.postgres.getConnect() }],
        //         },
        //         record.operations,
        //     )
        //     this.store = fortune(record.model, option)
        //
        // } else {
        //     throw new Error("Server Config Postgres Is Null")
        // }

    }

    async open() {
        return await this.store.connect()
    }

    async close() {
        return await this.store.disconnect()
    }

    async create(type: string, records: any, include?: any, meta?: any): Promise<any> {
        return await this.store.create(type, records, include, meta)
    }

    async delete(type: string, ids: any, include?: any, meta?: any): Promise<any> {
        return await this.store.delete(type, ids, include, meta)
    }

    async find(type: string, ids?: any, options?: any, include?: any, meta?: any): Promise<any> {
        return await this.store.find(type, ids, options, include, meta)
    }

    async update(type: string, updates: any, include?: any, meta?: any): Promise<any> {
        return await this.store.update(type, updates, include, meta)
    }
}
