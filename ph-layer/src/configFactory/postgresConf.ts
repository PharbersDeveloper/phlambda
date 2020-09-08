"use strict"
import {JsonObject, JsonProperty} from "json2typescript"
import {DBConf} from "./dbConf"

@JsonObject("PostgresConf")
export class PostgresConf extends DBConf {

    @JsonProperty("algorithm", String)
    public algorithm: string = undefined

    @JsonProperty("host", String)
    public host: string = undefined

    @JsonProperty("port", Number)
    public port: number = undefined

    @JsonProperty("username", String)
    public username: string = undefined

    @JsonProperty("pwd", String)
    public pwd: string = undefined

    @JsonProperty("dbName", String)
    public dbName: string = undefined

    public getUrl(): string {
        return `${this.algorithm}://${this.username}:${this.pwd}@${this.host}:${this.port}/${this.dbName}`
    }
}
