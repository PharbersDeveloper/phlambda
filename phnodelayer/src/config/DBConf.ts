"use strict"

export abstract class DBConf {
    public dbName: string = undefined

    public host: string = undefined

    public port: number = undefined

    public poolMax: number = undefined

    public idleTimeoutMillis: number = undefined

    public connectionTimeoutMillis: number = undefined

    public entry: string = undefined

    public username: string = undefined

    public pwd: string = undefined

    public abstract getUrl(): string

    public getConnect(): any {
        return {
            database: this.dbName,
            user: this.username,
            password: this.pwd,
            host: this.host,
            port: this.port,
            ssl: false,
            max: this.poolMax,
            idleTimeoutMillis: this.idleTimeoutMillis,
            connectionTimeoutMillis: this.connectionTimeoutMillis,
        }
    }
}
