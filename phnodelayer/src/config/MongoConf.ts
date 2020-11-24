"use strict"
import { DBConf } from "./DBConf"
// TODO: MongoDB有点问题，谁来接这个坑呢？
export default class MongoConf extends DBConf {
    public authSource: string = undefined
    public auth: boolean = false
    public other: string = undefined
    // constructor(entry: string,
    //             userName: string,
    //             pwd: string,
    //             host: string,
    //             port: number,
    //             dbName: string,
    //             other: string,
    //             poolMax: number,
    //             idleTimeoutMillis: number,
    //             connectionTimeoutMillis: number) {
    //     super()
    //     this.entry = entry
    //     this.username = userName
    //     this.pwd = pwd
    //     this.host = host
    //     this.port = port
    //     this.dbName = dbName
    //     this.other = other
    //     this.poolMax = poolMax
    //     this.idleTimeoutMillis = idleTimeoutMillis
    //     this.connectionTimeoutMillis = connectionTimeoutMillis
    // }
    public getUrl(): string {
        return `mongodb+srv://${this.username}:${this.pwd}@${this.host}/${this.dbName}${this.other}`
    }
}
