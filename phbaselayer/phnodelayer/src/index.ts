import phLogger from "./logger/PhLogger"
import App from "./delegate/appLambdaDelegate"
import { StoreEnum } from "./common/StoreEnum"
import StoreFactory from "./strategies/store/StoreFactory"
import AWSReq from "./strategies/AwsRequest"
import PostgresConf from "./config/PostgresConf"
import MongoConf from "./config/MongoConf"
import RedisConf from "./config/RedisConf"
import ConfRegistered from "./config/ConfRegistered"
import {IStore} from "./strategies/store/Store"

export const Logger = phLogger
export const Store = StoreEnum
export const SF = StoreFactory
export const AWSRequest = AWSReq
export const ConfigRegistered = ConfRegistered
export const PostgresConfig = PostgresConf
export const MongoConfig = MongoConf
export const RedisConfig = RedisConf

// @ts-ignore
export const JsonApiMain = async ({
    event = null,
    db = null,
}:{
    event: Map<string, any>,
    db: any,
} = {}) => {
    let result = null
    let del = null

    try {
        del = new App()
        del.prepare(db)
        if (event !== null && event !== undefined) {
            Logger.debug("开始执行请求")
            result = await del.exec(event)
            Logger.debug("执行请求结束")
        }
        return result
    } catch (e) {
        throw e
    }
}

// export const Main = async (event: Map<string, any>, db: any = Store.Postgres) => {
//     let result = null
//     let del = null
//     try {
//         Logger.debug("进入初始化")
//         del = new App()
//         if (del.isFirstInit) {
//             Logger.debug("准备初始化数据开始")
//             del.prepare(db)
//             Logger.debug("准备初始化数据结束")
//             Logger.debug("开始连接数据库")
//             await del.store.open()
//             Logger.debug("连接数据库结束")
//         }
//         if (event !== null && event !== undefined) {
//             Logger.debug("开始执行请求")
//             result = await del.exec(event)
//             Logger.debug("执行请求结束")
//         }
//         return result
//     } catch (e) {
//         throw e
//     } finally {
//         if (del !== null) {
//             del.isFirstInit = true
//             Logger.debug("关闭数据库开始")
//             await del.store.close()
//             Logger.debug("关闭数据库结束")
//         }
//     }
// }
