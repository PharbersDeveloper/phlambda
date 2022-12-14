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

// export const PostgresConf: IPhConf = {
//     name: StoreEnum.POSTGRES,
//     entity: "platform",
//     database: "phplatform_dev",
//     user: "pharbers_dev",
//     password: "123456",
//     // host: "localhost",
//     // port: 5432,
//     host: "ph-db-lambda-2021-11-15.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
//     port: 5432,
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

export const AWSRegion = "cn-northwest-1"
