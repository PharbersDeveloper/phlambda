"use strict"
import {JsonObject, JsonProperty} from "json2typescript"
import { PermissionsConf } from "./PermissionsConf"

@JsonObject("ServerConf")
export class ServerConf {

    @JsonProperty("permissions", PermissionsConf)
    public permissions: PermissionsConf = undefined
}