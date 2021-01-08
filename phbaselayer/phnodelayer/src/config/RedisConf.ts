"use strict"
import { DBConf } from "./DBConf"

export default class RedisConf extends DBConf {
    constructor(entry: string,
                userName: string,
                pwd: string,
                host: string,
                port: number,
                dbName: string,
                poolMax: number = 1,
                idleTimeoutMillis: number = 1000 ,
                connectionTimeoutMillis: number = 1000) {
        super()
        this.entry = entry
        this.username = userName
        this.pwd = pwd
        this.host = host
        this.port = port
        this.dbName = dbName
        this.poolMax = poolMax
        this.idleTimeoutMillis = idleTimeoutMillis
        this.connectionTimeoutMillis = connectionTimeoutMillis
    }

    public getUrl(): string {
        return `redis://${this.host}:${this.port}/${this.dbName}`
    }
}
