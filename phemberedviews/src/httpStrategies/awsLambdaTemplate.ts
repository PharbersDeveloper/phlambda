
import {ServerResponse} from "http"
import {APIController, DocumentationController} from "json-api"
import API from "json-api/build/src/controllers/API"
import Base, {HTTPStrategyOptions} from "json-api/build/src/http-strategies/Base"
import Controller from "json-api/build/src/http-strategies/Base"
import {
    ErrorOrErrorArray,
    HTTPResponse,
    Request as JSONAPIRequest,
    Result
} from "json-api/build/src/types/index"
import R = require("ramda")
import phLogger from "../logger/phLogger"
import phS3Facade from "../s3facade/phS3Facade"
import AWSLambdaStrategy from "./awsLambda"
import AWSReq from "./awsRequest"

/**
 * This controller receives requests directly from AWS Lambda and sends responses
 * directly through it, but it converts incoming requests to, and generates
 * responses, from Request and Response objects that are defined by this
 * framework in a way that's not particular to express. This controller thereby
 * acts as a translation-layer between express and the rest of this json-api
 * framework.
 *
 * @param {Object} options A set of configuration options.
 *
 * @param {boolean} options.tunnel Whether to turn on PATCH tunneling. See:
 *    http://jsonapi.org/recommendations/#patchless-clients
 *
 * @param {string} options.host The host that the API is served from, as you'd
 *    find in the HTTP Host header. This value should be provided for security,
 *    as the value in the Host header can be set to something arbitrary by the
 *    client. If you trust the Host header value, though, and don't provide this
 *    option, the value in the Header will be used.
 *
 * @param {boolean} options.handleContentNegotiation If the JSON API library
 *    can't produce a representation for the response that the client can
 *    `Accept`, should it return 406 or should it hand the request back to
 *    Express (i.e. call next()) so that subsequent handlers can attempt to
 *    find an alternate representation? By default, it does the former. But you
 *    can set this option to false to have this code just pass on to Express.
 */
export default class AWSHbsTemplateStrategy extends AWSLambdaStrategy {

    constructor(apiController: APIController,
                docsController?: DocumentationController,
                options?: HTTPStrategyOptions) {
        super(apiController, docsController, options)
    }

    public async doRequest(req: AWSReq, res: ServerResponse): Promise<HTTPResponse> {
        try {
            const requestObj = await this.buildRequestObject(req)
            phLogger.info(requestObj)
            const responseObj = await this.api.handle(requestObj, req, res)
            const hbs = JSON.parse(responseObj.body).data.attributes.hbs
            const result = await phS3Facade.getObject("ph-cli-dag-template", hbs)
            responseObj.body = result.toString()
            responseObj.headers = { "content-type": "text/x-handlebars-template"}
            return this.sendResponse(responseObj)
        } catch (err) {
            // This case should only occur if building a request object fails, as the
            // controller should catch any internal errors and always returns a response.
            return this.sendError(err, req) // , res, next)
        }
    }

    protected sendResponse(responseObj: HTTPResponse): HTTPResponse {
        return responseObj
    }

    protected async sendError(errors: ErrorOrErrorArray, req: AWSReq): Promise<HTTPResponse> {
        const responseObj = await API.responseFromError(errors, req.headers.accept)
        return responseObj
    }
}
