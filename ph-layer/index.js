
module.exports.phLogger = require('./dist/logger/phLogger').default
// module.exports.SingletonConf = require('./dist/configFactory/singletonConf').SingletonInitConf
module.exports.StoreEnum = require('./dist/common/StoreEnum').StoreEnum

module.exports.Main = async function (se, event) {
    const app = require('./dist/delegate/appLambdaDelegate').default
    const del = new app()
    let res
    if (del.isFirstInit) {
        await del.prepare(se)
    }
    if (event != null) {
        res = await del.exec(event)
    }
    await del.cleanUp()
    return res
}
