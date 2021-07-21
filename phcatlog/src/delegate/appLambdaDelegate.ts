import { ServerResponse } from "http"
import { identify } from "phauthlayer"
import { AWSRequest, ConfigRegistered, Logger, RedisConfig, SF, Store } from "phnodelayer"
import {RedisConf} from "../common/config"
import GetGlueData from "../common/getGlueData"
import ModelSerialize from "../common/modelSerialize"
import Register from "../common/register"
import {AWsGlue} from "../utils/AWSGlue"
import {AWSSts} from "../utils/AWSSts"

export default class AppLambdaDelegate {
    async exec(event: any) {
        ConfigRegistered.getInstance.registered(new RedisConfig(
            RedisConf.entry, RedisConf.user, RedisConf.password,
            RedisConf.url, RedisConf.port, RedisConf.db
        ))
        const rds = SF.getInstance.get(Store.Redis)
        await rds.open()
        const tokenResult = await rds.find("access", null, {match: {token: event.headers.Authorization}})
        try {
            const projectName = "catlog"
            const awsRequest = new AWSRequest(event, projectName)
            const awsResponse = new ServerResponse(awsRequest)

            const sts = new AWSSts()
            const result = await sts.assumeRole("AKIAWPBDTVEAI6LUCLPX",
                "Efi6dTMqXkZQ6sOpmBZA1IO1iu3rQyWAbvKJy599")
            const glueIns = new AWsGlue(result.AccessKeyId, result.SecretAccessKey, result.SessionToken)
            const getGlueData = new GetGlueData()

            const register = Register.getInstance
            register.registerEntity(projectName)
            register.registerFunction("databases", getGlueData.getDataBases)
            register.registerFunction("tables", getGlueData.getTables)
            register.registerFunction("partitions", getGlueData.getPartitions)

            let scope = ""
            if (tokenResult.payload.records.length > 0) {
                scope  = tokenResult.payload.records[0].scope
            }
            const flag = identify(event, scope)
            if (flag.status === 200) {
                if (!event.body) {
                    event.body = ""
                }
                const endpoint = event.pathParameters.type
                const queryStringParameters = event.queryStringParameters

                if (endpoint === "databases") {
                    const data = await register.getFunc(endpoint)(glueIns)
                    awsResponse["output"] = ["", JSON.stringify(new ModelSerialize().serialize(endpoint, data))]
                } else if (endpoint === "tables") {
                    const data = await register.getFunc(endpoint)(glueIns, queryStringParameters["filter[database]"])
                    awsResponse["output"] = ["", JSON.stringify(new ModelSerialize().serialize(endpoint, data))]
                } else {
                    const data = await register.getFunc(endpoint)(glueIns,
                        queryStringParameters["filter[database]"],
                        queryStringParameters["filter[table]"])
                    awsResponse["output"] = ["", JSON.stringify(new ModelSerialize().serialize(endpoint, data))]
                }
                return awsResponse
            }
            return flag
        } catch (error) {
            throw error
        } finally {
            await rds.close()
        }
    }
}
