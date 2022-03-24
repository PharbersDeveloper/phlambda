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
    readonly ssl: false,
    readonly idleTimeoutMs: number,
    readonly connectionTimeoutMs: number
}

export const MS_IN_S = 1_000

export const RedisConf: IPhConf = {
    name: StoreEnum.REDIS,
    entity: "db/token",
    database: "0",
    user: "",
    password: "",
    host: "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn",
    port: 6379,
    poolMax: 1,
    ssl: false,
    idleTimeoutMs: 10000,
    connectionTimeoutMs: 5000
}

export const PostgresConf: IPhConf = {
    name: StoreEnum.POSTGRES,
    entity: "db/oauth",
    database: "phplatform_dev",
    user: "pharbers_dev",
    password: "Abcde196125",
    host: "ph-db-lambda-2021-11-15.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
    port: 5432,
    poolMax: 1,
    ssl: false,
    idleTimeoutMs: 10000,
    connectionTimeoutMs: 5000
}

export const AccountUri = {
    uri: "https://accounts.pharbers.com/welcome"
}
