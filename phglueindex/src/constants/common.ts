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

export const PostgresConf: IPhConf = {
    name: StoreEnum.POSTGRES,
    entity: "index",
    database: "phentry",
    user: "pharbers",
    password: "Abcde196125",
    host: "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
    // host: "127.0.0.1",
    port: 5432,
    poolMax: 2
}

export const AWSRegion = "cn-northwest-1"
