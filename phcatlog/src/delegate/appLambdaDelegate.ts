import { ServerResponse } from "http"
import { AWSRequest } from "phnodelayer"
import GetGlueData from "../common/getGlueData"
import ModelSerialize from "../common/modelSerialize"
import Register from "../common/register"
import {AWsGlue} from "../utils/AWSGlue"
import {AWSSts} from "../utils/AWSSts"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            const projectName = "catlog"
            const awsRequest = new AWSRequest(event, projectName)
            const awsResponse = new ServerResponse(awsRequest)

            const sts = new AWSSts()
            const result = await sts.assumeRole(process.env.AccessKeyId,
                process.env.SecretAccessKey)
            const glueIns = new AWsGlue(result.AccessKeyId, result.SecretAccessKey, result.SessionToken)
            const getGlueData = new GetGlueData()

            const register = Register.getInstance
            register.registerEntity(projectName)
            register.registerFunction("databases", getGlueData.getDataBases)
            register.registerFunction("tables", getGlueData.getTables)
            register.registerFunction("partitions", getGlueData.getPartitions)

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
        } catch (error) {
            throw error
        }
    }
}
