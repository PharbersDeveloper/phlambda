import phLogger from "./logger/PhLogger"
import App from "./delegate/appLambdaDelegate"
import { StoreEnum } from "./common/StoreEnum"
import DBFactory from "./factory/DBFactory"
import RedisStore from "./strategies/store/RedisStore"
import AWSReq from "./strategies/AwsRequest"

export const logger = phLogger
export const store = StoreEnum
export const dbFactory = DBFactory
export const redis = RedisStore
export const AWSRequest = AWSReq

export const Main = async (event: Map<string, any>, db: any = StoreEnum.Postgres) => {
    let result = null
    let del = null
    try {
        logger.debug("进入初始化")
        del = new App()
        logger.debug("正在创建实例")

        if (del.isFirstInit) {
            logger.debug("开始连接数据库")
            await del.prepare(db)
            logger.debug("连接数据库结束")
        }

        if (event !== null && event !== undefined) {
            logger.debug("开始执行请求")
            result = await del.exec(event)
            logger.debug("执行请求结束")
        }
        logger.debug("关闭数据库")
        return result
    } catch (e) {
        throw e
    } finally {
        if (del !== null) {
            await del.cleanUp()
        }
    }
}
