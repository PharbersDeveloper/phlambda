"use strict"

import MongoDBAdapter from "fortune-mongodb"
import MySQLAdapter from "fortune-mysql"
import PostgresAdapter from "fortune-postgres"
import RedisAdapter from "fortune-redis"
import { StoreEnum } from "./StoreEnum"

export class Adapter {
    private static instance: Adapter = null
    private adapterMapping: Map<string, any> = new Map()

    constructor() {
        this.adapterMapping.set(StoreEnum.Postgres, PostgresAdapter)
        this.adapterMapping.set(StoreEnum.MongoDB, MongoDBAdapter)
        this.adapterMapping.set(StoreEnum.Mysql, MySQLAdapter)
        this.adapterMapping.set(StoreEnum.Redis, RedisAdapter)
    }

    public static get init() {
        if (Adapter.instance === null) {
            Adapter.instance = new Adapter()
        }
        return Adapter.instance
    }

    public getAdapter(name: string): any {
        return this.adapterMapping.get(name)
    }
}
