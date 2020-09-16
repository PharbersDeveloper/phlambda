
const se = require('./dist/common/StoreEnum').StoreEnum
const logger = require('./dist/logger/phLogger').default
module.exports.phLogger = logger
module.exports.StoreEnum = se
module.exports.DBFactory = require("./dist/dbFactory/DBFactory").default

module.exports.Main = async function (event, store = se.Postgres) {
    logger.debug("进入初始化")
    const app = require('./dist/delegate/appLambdaDelegate').default
    const del = new app()
    logger.debug("正在创建实例")
    let res
    if (del.isFirstInit) {
        logger.debug("开始连接数据库")
        await del.prepare(store)
        logger.debug("连接数据库结束")
    }
    if (event != null) {
        logger.debug("开始执行请求")
        res = await del.exec(event)
    }
    await del.cleanUp()
    logger.debug("关闭数据库连接")
    return res
}
