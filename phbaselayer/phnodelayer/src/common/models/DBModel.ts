import BaseModel from "../models/BaseModel"
import { StoreEnum } from "../enum/StoreEnum"

export default class DBModel extends BaseModel {
    public name: string
    private readonly database: string
    private readonly user: string
    private readonly password: string
    private readonly host: string
    private readonly port: number
    private readonly ssl: boolean = false
    private readonly max: number
    private readonly idleTimeoutMillis: number
    private readonly connectionTimeoutMillis: number

    constructor({
        name = null,
        database = null,
        user = null,
        password = null,
        host = null,
        port = 0,
        max = 0,
        ssl = false,
        idleTimeoutMillis = 1000,
        connectionTimeoutMillis = 1000
    }: {
        name: string,
        database: string,
        user: string,
        password: string,
        host: string,
        port: number,
        max: number,
        ssl?: boolean,
        idleTimeoutMillis?: number,
        connectionTimeoutMillis?: number
    }) {
        super()
        this.name = name
        this.database = database
        this.user = user
        this.password = password
        this.host = host
        this.port = port
        this.ssl = ssl
        this.max = max
        this.idleTimeoutMillis = idleTimeoutMillis
        this.connectionTimeoutMillis = connectionTimeoutMillis
    }

    toString(): string {
        return ""
    }

    toStructure(): any {
        switch(this.name) {
            case StoreEnum.POSTGRES:
                return {
                    connection: {
                        name: this.name,
                        database: this.database,
                        user: this.user,
                        password: this.password,
                        host: this.host,
                        port: this.port,
                        ssl: this.ssl,
                        max: this.max,
                        idleTimeoutMillis: this.idleTimeoutMillis,
                        connectionTimeoutMillis: this.connectionTimeoutMillis,
                    }
                }
            case StoreEnum.REDIS:
                return {
                    name: this.name,
                    host: this.host,
                    port: this.port,
                    options: {
                        db: this.database,
                        username: this.user,
                        password: this.password,
                        commandTimeout: this.idleTimeoutMillis,
                        connectTimeout: this.connectionTimeoutMillis,
                    }
                }
            case StoreEnum.MONGO:
                return {
                    connection: {
                        name: this.name,
                        database: this.database,
                        user: this.user,
                        password: this.password,
                        host: this.host,
                        port: this.port,
                        ssl: this.ssl,
                        max: this.max,
                        idleTimeoutMillis: this.idleTimeoutMillis,
                        connectionTimeoutMillis: this.connectionTimeoutMillis,
                    }
                }
        }
        return {
            name: this.name,
            database: this.database,
            user: this.user,
            password: this.password,
            host: this.host,
            port: this.port,
            ssl: this.ssl,
            max: this.max,
            idleTimeoutMillis: this.idleTimeoutMillis,
            connectionTimeoutMillis: this.connectionTimeoutMillis,
        }
    }
}

