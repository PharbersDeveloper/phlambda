import BaseModel from "../models/BaseModel"
import DBModel from "../models/DBModel"
import Config from "./Config"


export default class DBConfig extends Config {
    public name: string
    // private protocols: string
    public readonly entity: string
    private readonly database: string
    private readonly host: string
    private readonly port: number
    private readonly poolMax: number
    private readonly idleTimeoutMs: number
    private readonly connectionTimeoutMs: number
    private readonly user: string
    private readonly password: string
    private readonly ssl: boolean
    // private other: string

    constructor({
        name = null,
        entity = null,
        database = null,
        user = null,
        password = null,
        host = null,
        port = 0,
        poolMax = 1,
        ssl = false,
        idleTimeoutMs = 1000,
        connectionTimeoutMs = 1000
    }: {
        name: string,
        entity: string,
        database: string,
        user: string,
        password: string,
        host: string,
        port: number,
        poolMax?: number,
        ssl?: boolean,
        idleTimeoutMs?: number,
        connectionTimeoutMs?: number
    }) {
        super()
        this.name = name
        this.entity = entity
        this.database = database
        this.user = user
        this.password = password
        this.host = host
        this.port = port
        this.poolMax = poolMax
        this.ssl = ssl
        this.idleTimeoutMs = idleTimeoutMs
        this.connectionTimeoutMs = connectionTimeoutMs
    }

    getConf(): BaseModel {
        return new DBModel({
            name: this.name,
            database: this.database,
            user: this.user,
            password: this.password,
            host: this.host,
            port: this.port,
            ssl: this.ssl,
            max: this.poolMax,
            idleTimeoutMillis: this.idleTimeoutMs,
            connectionTimeoutMillis: this.connectionTimeoutMs
        })
    }

    toString(): string {
        return ""
    }

    toStructure(): any {
        return this.getConf().toStructure()
    }
}
