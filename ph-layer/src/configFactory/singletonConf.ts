"use strict"

import * as fs from "fs"
import * as yaml from "js-yaml"
import {JsonConvert, ValueCheckingMode} from "json2typescript"
import phLogger from "../logger/phLogger"
import { ServerConf } from "./serverConf"

export class SingletonInitConf {
    private static conf: ServerConf

    private static init() {
        if (!SingletonInitConf.conf) {
            const path = `${process.cwd()}/config/server.yml`
            const jsonConvert = new JsonConvert()
            const doc = yaml.safeLoad(fs.readFileSync(path, "utf8"))
            jsonConvert.ignorePrimitiveChecks = false
            jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL
            SingletonInitConf.conf = jsonConvert.deserializeObject(doc, ServerConf)
        }
    }

    constructor() {
        if (!SingletonInitConf.conf) { SingletonInitConf.init() }
    }

    public getConf() {
        return SingletonInitConf.conf
    }
}
