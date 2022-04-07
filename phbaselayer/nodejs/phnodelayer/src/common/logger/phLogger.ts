"use strict"

import * as fs from "fs"
import { configure, getLogger } from "log4js"

class PhLogger {
    constructor() {
        let path = `${process.cwd()}/config/log4js.json`
        if (!fs.existsSync(path)) {
            path = `${__filename.substring(0, __filename.indexOf("lib"))}config/log4js.json`
        }
        configure(path)
    }

    public getPhLogger() {
        return getLogger()
    }
}

export default new PhLogger().getPhLogger()
