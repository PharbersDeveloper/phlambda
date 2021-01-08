"use strict"
import {JsonObject, JsonProperty} from "json2typescript"

@JsonObject("RedisConf")
export class RedisConf {

    @JsonProperty("algorithm", String)
    public algorithm: string = undefined

    @JsonProperty("host", String)
    public host: string = undefined

    @JsonProperty("port", Number)
    public port: number = undefined

    @JsonProperty("db", Number)
    public db: string = undefined
}
