"use strict"
import {JsonObject, JsonProperty} from "json2typescript"
import { MongoConf } from "./mongoConf"
import { MysqlConf } from "./mysqlConf"
import { PostgresConf } from "./postgresConf"

@JsonObject("ServerConf")
export class ServerConf {

    @JsonProperty("project", String)
    public project: string = undefined

    @JsonProperty("mongo", MongoConf)
    public mongo: MongoConf = undefined

    @JsonProperty("postgres", PostgresConf)
    public postgres: PostgresConf = undefined

    @JsonProperty("mysql", MysqlConf)
    public mysql: MysqlConf = undefined
}
