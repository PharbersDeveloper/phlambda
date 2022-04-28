import { ServerResponse } from "http"
import { AWSRequest, DBConfig, JSONAPI, Logger, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import { PostgresConf } from "../constants/common"
import FindGlueTableHandler from "../handler/FindGlueTableHandler"
import TransformData from "../utils/adapter/TransformData"

class GlueTableDelegate {
    async run(event: any) {
        const paths = event.path.split("/")
        const projectName = paths[0] === "" ? paths[1] : paths[0]
        const awsRequest = new AWSRequest(event, projectName)
        const awsResponse = new ServerResponse(awsRequest)
        const body = JSON.parse(event.body)
        const database = body.projectId
        const table = body.dsName
        const result = await new FindGlueTableHandler().findTable(database, table)
        const jsonData = new TransformData().run("tables", result)
        awsResponse["outputData"] = [{data: ""}, {data: JSON.stringify(jsonData)}]
        return awsResponse
    }
}

// tslint:disable-next-line:max-classes-per-file
class JsonapiDelegate {
    async run(event: any) {
        ServerRegisterConfig([ new DBConfig(PostgresConf) ])
        return await JSONAPI(StoreEnum.POSTGRES, event)
    }
}

// tslint:disable-next-line:max-classes-per-file
export default class FunctionDelegate {
    private links = {
        default: JsonapiDelegate,
        catlog_post: GlueTableDelegate
    }

    async run(event: any) {
        const type = event.pathParameters.type
        const method = event.httpMethod
        const key = `${type}_${method}`.toLocaleLowerCase()
        const endpoint = key === "catlog_post" ? key : "default"
        const instance = new this.links[endpoint]()
        return await instance.run(event)
    }
}
