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
    entity: "max",
    database: "phmax",
    user: "pharbers",
    password: "Abcde196125",
    host: "192.168.49.199",
    port: 5442,
    poolMax: 1,
    ssl: false,
    idleTimeoutMs: 3000,
    connectionTimeoutMs: 3000
}

export const AWSRegion = "cn-northwest-1"