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
    redis: any = null
    async exec(event: any) {
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

        const rds = new RedisConfig(
            RedisConf.entry, RedisConf.user, RedisConf.password,
            RedisConf.url, RedisConf.port, RedisConf.db
        )
        ConfigRegistered.getInstance.registered(rds)
        this.redis = SF.getInstance.get(Store.Redis)
        // await this.redis.open()
        try {
            if (!event.body) {
                event.body = ""
            }
            const endpoint = event.pathParameters.edp
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
        } catch (error) {
            throw error
        } finally {
            // await this.redis.close()
        }
    }
}
