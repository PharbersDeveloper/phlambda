"use strict"
import {JsonObject, JsonProperty} from "json2typescript"
import { ModelConf } from "./modelConf"
import { MongoConf } from "./mongoConf"

@JsonObject("ServerConf")
export class ServerConf {

    @JsonProperty("project", String)
    public project: string = undefined

    @JsonProperty("models", [ModelConf])
    public models: ModelConf[] = undefined

    @JsonProperty("mongo", MongoConf)
    public mongo: MongoConf = undefined
}
