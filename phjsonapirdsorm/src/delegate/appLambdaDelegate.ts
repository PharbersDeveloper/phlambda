import { identify } from "phauthlayer"
import { ConfigRegistered, Logger, Main, PostgresConfig, RedisConfig, SF, Store } from "phnodelayer"
import { modelConvert } from "../handler/modelConvertHandler"
import { modelExport } from "../handler/modelExportHandler"
import { modelExportOffwebExcel } from "../handler/modelExportOffwebExcel"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        // @ts-ignore
        if (event.pathParameters.type === "convert") {
            return await modelConvert(event)
        }
        // @ts-ignore
        if (event.pathParameters.type === "export") {
            return await modelExport(event)
        }

        const pg = new PostgresConfig("offweb", "pharbers", "Abcde196125", "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn", 5432, "phoffweb")
        // const redis =
        // new RedisConfig("token", "", "", "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn", 6379, "0")
        // ConfigRegistered.getInstance.registered(pg).registered(redis)
        // const rds = SF.getInstance.get(Store.Redis)
        // await rds.open()
        // // @ts-ignore
        // const result = await rds.find("access", null, {match: {token: event.headers.Authorization}})
        // await rds.close()
        // let scope = ""
        // if (result.payload.records.length > 0) {
        //     scope  = result.payload.records[0].scope
        // }
        // const flag = identify(event, scope)
        // if (flag.status === 200) {
        //     return await Main(event)
        // }
        // return flag
        ConfigRegistered.getInstance.registered(pg)
        // @ts-ignore
        if (event.pathParameters.type === "exports") {
            return await modelExportOffwebExcel(event)
        }
        return await Main(event)
    }
}
