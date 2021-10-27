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

export const PostgresConf: IPhConf = {
    name: StoreEnum.POSTGRES,
    entity: "index",
    database: "phplatform",
    user: "pharbers",
    password: "Abcde196125",
    host: "192.168.49.199",
    port: 5439,
    // host: "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
    // port: 5432,
    poolMax: 1,
    ssl: false,
    idleTimeoutMs: 10000,
    connectionTimeoutMs: 5000
}

export const AWSRegion = "cn-northwest-1"
