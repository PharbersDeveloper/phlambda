import { ServerResponse } from "http"
import { AWSRequest, DBConfig, JSONAPI, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import PagePartitionHandler from "../handler/PagePartitionHandler"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            const endpoint = event.pathParameters.type
            const configs = [
                new DBConfig({
                    name: StoreEnum.POSTGRES,
                    entity: "catlog",
                    database: "phentry",
                    user: "pharbers",
                    password: "Abcde196125",
                    host: "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
                    port: 5432,
                    poolMax: 2
                })
            ]
            if (endpoint === "partitions") {
                const paths = event.path.split("/")
                const projectName = paths[0] === "" ? paths[1] : paths[0]
                const awsRequest = new AWSRequest(event, projectName)
                const awsResponse = new ServerResponse(awsRequest)
                const result = await new PagePartitionHandler().pageFind(
                    event.queryStringParameters["filter[database]"],
                    event.queryStringParameters["filter[table]"],
                    event.queryStringParameters["nextToken"],
                    Number(event.queryStringParameters["page[limit]"]))
                awsResponse["outputData"] = [{data: ""}, {data: JSON.stringify(result)}]
                return awsResponse
            }
            ServerRegisterConfig(configs)
            return JSONAPI(StoreEnum.POSTGRES, event)
        } catch (error) {
            throw error
        }
    }
}
