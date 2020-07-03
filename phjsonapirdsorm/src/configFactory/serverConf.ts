"use strict"
import {JsonObject, JsonProperty} from "json2typescript"
import { MongoConf } from "./mongoConf"

@JsonObject("ServerConf")
export class ServerConf {

    @JsonProperty("project", String)
    public project: string = undefined

    @JsonProperty("mongo", MongoConf)
    public mongo: MongoConf = undefined
}
