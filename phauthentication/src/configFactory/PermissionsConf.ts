"use strict"
import {JsonObject, JsonProperty} from "json2typescript"

@JsonObject("PermissionsConf")
export class PermissionsConf {

    @JsonProperty("values", [String])
    public values: string[] = undefined
}
