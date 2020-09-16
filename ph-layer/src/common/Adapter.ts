"use strict"

import MongoDBAdapter from "fortune-mongodb"
import MySQLAdapter from "fortune-mysql"
import PostgresAdapter from "fortune-postgres"
import RedisAdapter from "fortune-redis"
import { ServerConf } from "../configFactory/ServerConf"
import phLogger from "../logger/phLogger"
import { StoreEnum } from "./StoreEnum"

export class Adapter {
    private static instance: Adapter = null
    private adapterMapping: Map<string, any> = new Map()

    constructor(conf?: ServerConf) {
        this.adapterMapping.set(StoreEnum.Postgres, PostgresAdapter)
        this.adapterMapping.set(StoreEnum.MongoDB, MongoDBAdapter)
        this.adapterMapping.set(StoreEnum.Mysql, MySQLAdapter)
        this.adapterMapping.set(StoreEnum.Redis, RedisAdapter)
        // for (const name of Object.getOwnPropertyNames(conf)) {
        //     const ins = conf[name]
        //     if (ins !== undefined && typeof ins !== "string") {
        //        switch (name) {
        //            case "postgres":
        //                this.adapterMapping.set(name, PostgresAdapter)
        //                break
        //            case "mongo":
        //                this.adapterMapping.set(name, MongoDBAdapter)
        //                break
        //            case "mysql":
        //                this.adapterMapping.set(name, MySQLAdapter)
        //                break
        //            case "redis":
        //                this.adapterMapping.set(name, RedisAdapter)
        //                break
        //            default:
        //                phLogger.info("没有")
        //                break
        //        }
        //     }
        // }
    }

    public static get init() {
        if (Adapter.instance == null) {
            Adapter.instance = new Adapter()
        }
        return Adapter.instance
    }

    public getAdapter(name: string): any {
        return this.adapterMapping.get(name)
    }

}
