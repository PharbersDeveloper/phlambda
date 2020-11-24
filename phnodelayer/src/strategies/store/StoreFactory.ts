"use strict"

import ServerConf from "../../config/ServerConf"
import PostgresStore from "./PostgresStore"
import RedisStore from "./RedisStore"

export default class StoreFactory {
    private static instance: StoreFactory = null
    private typeAnalyzerMapping: Map<string, any> = new Map()

    private constructor(serverConf: ServerConf) {
        this.buildStore(serverConf)
    }

    public static getInstance(serverConf?: ServerConf) {
        if (StoreFactory.instance == null) {
            StoreFactory.instance = new StoreFactory(serverConf)
        }
        return StoreFactory.instance
    }

    public get(name?: string): any {
        if (name === undefined || name === null || name.length === 0) {
            if (this.typeAnalyzerMapping.size === 1) {
                return [...this.typeAnalyzerMapping.values()][0]
            } else {
                throw new Error(
                    `存在多个Store, 请使用 getStore(参数) 获取对应Store，包含参数：${[
                        ...this.typeAnalyzerMapping.keys(),
                    ]}`,
                )
            }
        }
        return this.typeAnalyzerMapping.get(name)
    }

    private buildStore(conf: ServerConf) {
        const storeTargets = Object.getOwnPropertyNames(conf)
            .map((name: string) => {
                const ins = conf[name]
                if (ins !== undefined && ins !== null && name !== "project") {
                    return name
                }
            })
            .filter((item) => item !== undefined && item !== null)

        for (const target of storeTargets) {
            if (target === "postgres" && !this.typeAnalyzerMapping.has(target)) {
                this.typeAnalyzerMapping.set(target, new PostgresStore(conf))
            } else if (target === "redis" && !this.typeAnalyzerMapping.has(target)) {
                this.typeAnalyzerMapping.set(target, new RedisStore(conf))
            }
        }
    }
}
