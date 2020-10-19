"use strict"
import {JsonObject, JsonProperty} from "json2typescript"
import { DBConf } from "./DBConf"

@JsonObject("MysqlConf")
export class MysqlConf extends DBConf {

    @JsonProperty("dbName", String)
    public dbName: string = undefined

    public getUrl(): string {
        return `${this.algorithm}://${this.username}:${this.pwd}@${this.host}:${this.port}/${this.dbName}`
    }

}
