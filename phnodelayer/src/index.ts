import phLogger from "./logger/PhLogger"
import App from "./delegate/appLambdaDelegate"
import { StoreEnum } from "./common/StoreEnum"
import DBFactory from "./factory/DBFactory"
import Redis from "./strategies/store/RedisStore"

export const logger = phLogger
export const store = StoreEnum
export const dbFactory = DBFactory
export const redis = Redis

export const Main = async (event: Map<string, any>, db: any = StoreEnum.Postgres) => {
	logger.debug("进入初始化")
	const del = new App()
	logger.debug("正在创建实例")

	let result = null

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

	await del.cleanUp()
	logger.debug("关闭数据库")
	return result
}