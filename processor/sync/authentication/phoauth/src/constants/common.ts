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
    entity: process.env.REDISENTITY,
    database: process.env.REDISDATABASE,
    user: "",
    password: "",
    host: process.env.REDISHOST,
    port: Number(process.env.REDISPORT),
    poolMax: 1,
    ssl: false,
    idleTimeoutMs: 10000,
    connectionTimeoutMs: 5000
}

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
    idleTimeoutMs: 10000,
    connectionTimeoutMs: 5000
}

export const AccountUri = {
    uri: "https://accounts.pharbers.com/welcome"
}
