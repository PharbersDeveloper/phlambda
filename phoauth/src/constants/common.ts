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

export const MS_IN_S = 1_000

export const RedisConf: IPhConf = {
    name: StoreEnum.REDIS,
    entity: "db/token",
    database: "0",
    user: "",
    password: "",
    // host: "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn",
    host: "127.0.0.1",
    port: 6379,
    poolMax: 2
}

export const PostgresConf: IPhConf = {
    name: StoreEnum.POSTGRES,
    entity: "db/oauth",
    database: "phcommon",
    user: "pharbers",
    password: "Abcde196125",
    // host: "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
    host: "127.0.0.1",
    port: 5432,
    poolMax: 2
}

export const AccountUri = {
    uri: "https://accounts.pharbers.com/welcome"
}
