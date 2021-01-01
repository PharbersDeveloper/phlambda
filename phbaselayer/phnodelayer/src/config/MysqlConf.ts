"use strict"
import { DBConf } from "./DBConf"

export default class MysqlConf extends DBConf {
    constructor(entry: string,
                userName: string,
                pwd: string,
                host: string,
                port: number,
                dbName: string,
                poolMax: number,
                idleTimeoutMillis: number,
                connectionTimeoutMillis: number) {
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
        return `mysql://${this.username}:${this.pwd}@${this.host}:${this.port}/${this.dbName}`
    }
}
