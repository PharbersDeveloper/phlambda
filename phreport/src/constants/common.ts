import {  StoreEnum } from "phnodelayer"

export interface IPhConf {
    readonly name: string
    readonly entity: string
    readonly database: string
    readonly user: string
    readonly password: string
    readonly host: string
    readonly port: number
    readonly poolMax: number
}

export const RedisConf: IPhConf = {
    name: StoreEnum.REDIS,
    entity: "token",
    database: "0",
    user: "",
    password: "",
    // host: "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn",
    host: "127.0.0.1",
    port: 6379,
    poolMax: 2
}

export const PostgresConf: IPhConf = {
    name: StoreEnum.REDIS,
    entity: "reports",
    database: "phreports",
    user: "pharbers",
    password: "Abcde196125",
    // host: "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
    host: "127.0.0.1",
    port: 5432,
    poolMax: 2
}
