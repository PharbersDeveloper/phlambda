import { ServerResponse } from "http"
import { AWSRequest, DBConfig, JSONAPI, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import { AWSRegion, PostgresConf } from "../constants/common"
import GlueCatlogHandler from "../handler/GlueCatlogHandler"

export default class AppLambdaDelegate {
    async exec(event: any) {
        const endpoint = event.pathParameters.type
        const method = event.httpMethod.toLowerCase()
        try {
            ServerRegisterConfig([ new DBConfig(PostgresConf) ])
            if (endpoint === "findTableSchema" && method === "get") {
                const { table, database } = event.queryStringParameters
                const paths = event.path.split("/")
                const projectName = paths[0] === "" ? paths[1] : paths[0]
                const awsRequest = new AWSRequest(event, projectName)
                const awsResponse = new ServerResponse(awsRequest)
                const result = await new GlueCatlogHandler({
                    region: AWSRegion
                }).findTable(table, database)
                awsResponse["outputData"] = [{data: ""}, {data: JSON.stringify(result)}]
                return awsResponse
            }
            return JSONAPI(StoreEnum.POSTGRES, event)
        } catch (error) {
            throw error
        }
    }
}
