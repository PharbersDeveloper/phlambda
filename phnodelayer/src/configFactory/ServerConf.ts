"use strict"
import { JsonObject, JsonProperty } from "json2typescript"
import { MongoConf } from "./MongoConf"
import { MysqlConf } from "./MysqlConf"
import { PostgresConf } from "./PostgresConf"
import { RedisConf } from "./RedisConf"

@JsonObject("ServerConf")
export class ServerConf {

    @JsonProperty("project", String)
    public project: string = undefined

    @JsonProperty("postgres", PostgresConf)
    public postgres: PostgresConf = undefined

    @JsonProperty("mongo", MongoConf, true)
    public mongo: MongoConf = undefined

    @JsonProperty("mysql", MysqlConf, true)
    public mysql: MysqlConf = undefined

    @JsonProperty("redis", RedisConf, true)
    public redis: RedisConf = undefined
}
