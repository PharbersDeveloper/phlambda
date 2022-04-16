import BaseModel from "./BaseModel"
import Context from "../strategy/Context"

export default class DBModel extends BaseModel {
    public name: string
    public readonly database: string
    public readonly user: string
    public readonly password: string
    public readonly host: string
    public readonly port: number
    public readonly ssl: boolean = false
    public readonly max: number
    public readonly idleTimeoutMillis: number
    public readonly connectionTimeoutMillis: number

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
        const context = new Context(this)
        return context.doChoose()
    }
}

