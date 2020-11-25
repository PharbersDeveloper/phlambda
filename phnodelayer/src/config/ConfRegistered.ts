"use strict"

import { DBConf } from "./DBConf"
import Logger from "../logger/phLogger"

export default class ConfRegistered {
    private static instance: ConfRegistered = null
    private confMap: Map<string, any> = new Map()

    private constructor() {}


    registered(conf: DBConf): ConfRegistered {
        Logger.debug(`配置文件 ${conf.constructor.name} 已注册`)
        this.confMap.set(conf.constructor.name.toLowerCase(), conf)
        return this
    }

    getConf(name: string): DBConf {
        return this.confMap.get(name.toLowerCase())
    }

    static get getInstance() {
        if (ConfRegistered.instance === null) {
            ConfRegistered.instance = new ConfRegistered()
        }
        return ConfRegistered.instance
    }
}
