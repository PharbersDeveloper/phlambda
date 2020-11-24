"use strict"

import { Store, IStore } from "./Store"
import ServerConf from "../../config/ServerConf"
import PostgresAdapter from "fortune-postgres"
import fortune from "fortune"

export default class PostgresStore extends Store implements IStore {
    constructor(conf: ServerConf) {
        super()
        if (conf.postgres) {
            const record = new (this.getRecord(conf.postgres.entry))()
            const option = Object.assign(
                {
                    adapter: [PostgresAdapter, { connection: conf.postgres.getConnect() }],
                },
                record.operations,
            )
            this.store = fortune(record.model, option)

        } else {
            throw new Error("Server Config Postgres Is Null")
        }

    }

    async open() {
        return await this.store.connect()
    }

    async close() {
        return await this.store.disconnect()
    }

    async create(type: string, records: any, include: any, meta: any): Promise<any> {
        return await this.store.create(type, records, include, meta)
    }

    async delete(type: string, ids: any, include: any, meta: any): Promise<any> {
        return await this.store.delete(type, ids, include, meta)
    }

    async find(type: string, ids: any, options: any, include: any, meta: any): Promise<any> {
        return await this.store.find(type, ids, options, include, meta)
    }

    async update(type: string, updates: any, include: any, meta: any): Promise<any> {
        return await this.store.update(type, updates, include, meta)
    }
}
