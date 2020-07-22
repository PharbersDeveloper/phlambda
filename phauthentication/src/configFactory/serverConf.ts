"use strict"
import {JsonObject, JsonProperty} from "json2typescript"
import { MongoConf } from "./mongoConf"
import { PostgresConf } from "./postgresConf"
import {RedisConf} from "./redisConf"

@JsonObject("ServerConf")
export class ServerConf {

    @JsonProperty("project", String)
    public project: string = undefined

    @JsonProperty("mongo", MongoConf)
    public mongo: MongoConf = undefined

    @JsonProperty("postgres", PostgresConf)
    public postgres: PostgresConf = undefined

    @JsonProperty("redis", RedisConf)
    public redis: RedisConf = undefined
}
