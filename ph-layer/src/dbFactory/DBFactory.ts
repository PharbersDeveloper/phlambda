"use strict"

import fortune from "fortune"
import { Adapter } from "../common/Adapter"
import { InitServerConf } from "../common/InitServerConf"
import { StoreEnum } from "../common/StoreEnum"
import { ServerConf } from "../configFactory/ServerConf"
import phLogger from "../logger/phLogger"

export default class DBFactory {

    private static instance: DBFactory = null
    private typeAnalyzerMapping: Map<string, any> = new Map()
    private serverConf: ServerConf = InitServerConf.getConf

    constructor() {
        this.buildStore(this.serverConf)
    }

    public static get getInstance() {
        if (DBFactory.instance == null) {
            DBFactory.instance = new DBFactory()
        }
        return DBFactory.instance
    }

    // public register(se: StoreEnum, entry: string) {
    //     const ad = Adapter.init.getAdapter(se)
    //     const url = this.serverConf[se].getUrl()
    //     const filename = `${process.cwd()}/dist/models/${entry}.js`
    //     const record = require(filename).default
    //     this.typeAnalyzerMapping.set(se, fortune(record, {adapter: [ ad, {url}] }))
    // }

    public getStore(name?: string): any {
        if (name === undefined || name === null || name.length === 0) {
            if (this.typeAnalyzerMapping.size === 1) {
                return [...this.typeAnalyzerMapping.values()][0]
            } else {
                throw new Error(`存在多个Store, 请使用 getStore(参数) 获取对应Store，包含参数：${[...this.typeAnalyzerMapping.keys()]}`)
            }
        }
        return this.typeAnalyzerMapping.get(name)
    }

    private buildStore(conf: ServerConf): any {
        const keys = Object.getOwnPropertyNames(conf).map((name) => {
            const ins = conf[name]
            if (ins !== undefined && typeof ins !== "string") {
                return name
            }
        }).filter((item) => item !== undefined)

        let filename = null

        for (const key of keys) {
            const ad = Adapter.init.getAdapter(key)
            const url = conf[key].getUrl()
            const path = `${process.cwd()}/dist/models`
            if (conf[key].dao !== undefined) {
                filename = `${path}/${conf[key].dao}.js`
            } else {
                filename = `${path}/${conf.project}.js`
            }
            const record = require(filename).default
            this.typeAnalyzerMapping.set(key, fortune(record, {adapter: [ ad, {url}] }))
        }
    }

}
