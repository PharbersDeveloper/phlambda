import phLogger from "../../../phemberedviews/src/logger/phLogger"
import phS3Facade from "../../../phemberedviews/src/s3facade/phS3Facade"
import AWSReq from "../../../phjsonapirdsorm/src/strategies/awsRequest"
import AppLambdaDelegate from "./appLambdaDelegate"
import {ServerResponse} from "http"

export default class AppLambdaViewAgentDelegate extends AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        const response = await super.exec(event)
        // const hbs = JSON.parse(responseObj.body).data.attributes.hbs
        // const result = await phS3Facade.getObject("ph-cli-dag-template", hbs)
        // responseObj.body = result.toString()
        // responseObj.headers = { "content-type": "text/x-handlebars-template"}
        // return this.sendResponse(responseObj)
        return response
    }
}
