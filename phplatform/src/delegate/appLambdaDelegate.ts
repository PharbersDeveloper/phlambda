import { ServerResponse } from "http"
import { AWSRequest, DBConfig, JSONAPI, Logger, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import { PostgresConf } from "../constants/common"
import PagePartitionHandler from "../handler/PagePartitionHandler"

export default class AppLambdaDelegate {
    async exec(event: any) {
        try {
            const endpoint = event.pathParameters.type
            // TODO: 这个也要改
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
            ServerRegisterConfig([ new DBConfig(PostgresConf) ])
            return JSONAPI(StoreEnum.POSTGRES, event)
        } catch (error) {
            throw error
        }
    }
}
