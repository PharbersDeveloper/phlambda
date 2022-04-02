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

export const RedisConf: IPhConf = {
    name: StoreEnum.REDIS,
    entity: "act",
    database: "0",
    user: "",
    password: "",
    host: "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn",
    port: 6379,
    poolMax: 1,
    ssl: false,
    idleTimeoutMs: 3000,
    connectionTimeoutMs: 3000
}

// export const PostgresConf: IPhConf = {
//     name: StoreEnum.POSTGRES,
//     entity: "common",
//     database: "phplatform",
//     user: "pharbers",
//     password: "Abcde196125",
//     host: "192.168.49.199",
//     port: 5439,
//     poolMax: 1,
//     ssl: false,
//     idleTimeoutMs: 3000,
//     connectionTimeoutMs: 3000
// }

export const PostgresConf: IPhConf = {
    name: StoreEnum.POSTGRES,
    entity: process.env.ENTITY,
    database: process.env.DATABASE,
    user: process.env.USER,
    password: process.env.PASSWORD,
    host: process.env.HOST,
    port: Number(process.env.PORT),
    poolMax: 1,
    ssl: false,
    idleTimeoutMs: 3000,
    connectionTimeoutMs: 3000
}
