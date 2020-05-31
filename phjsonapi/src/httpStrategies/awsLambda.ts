
import {APIController, DocumentationController} from "json-api"
import Base, {HTTPStrategyOptions} from "json-api/build/src/http-strategies/Base"
import {
    ErrorOrErrorArray,
    HTTPResponse,
    Request as JSONAPIRequest,
    Result
} from "json-api/build/src/types/index"
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
export default class AWSLambdaStrategy extends Base {
    constructor(apiController: APIController,
                docsController?: DocumentationController,
                options?: HTTPStrategyOptions) {
        super(apiController, docsController, options)
    }

    /**
     * Builds a Request object from an IncomingMessage object. It is not
     * possible to infer the protocol or the url params from the IncomingMessage
     * object alone so they must be passed as arguments. Optionally a query object
     * can be passed, otherwise the query parameters will be inferred from the
     * IncomingMessage url property and parsed using the qs node module.
     *
     * @param {http.IncomingMessage} req original request object from core node module http
     * @param {string} protocol
     * @param {string} fallbackHost Host to use if strategy.options.host is not set
     * @param {Object} params object containing url parameters
     * @param {Object} [parsedQuery] object containing pre-parsed query parameters
     */
    public async buildRequestObject(req: AWSReq): Promise<JSONAPIRequest> {
        const genericReqPromise =
            // tslint:disable-next-line deprecation
            super.buildRequestObject(req, req.protocol, req.host, req.params, req.query)

        return genericReqPromise
    }
}
