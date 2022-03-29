"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const API_1 = __importDefault(require("json-api/build/src/controllers/API"));
const phLogger_1 = __importDefault(require("../logger/phLogger"));
const phS3Facade_1 = __importDefault(require("../s3facade/phS3Facade"));
const awsLambda_1 = __importDefault(require("./awsLambda"));
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
class AWSHbsTemplateStrategy extends awsLambda_1.default {
    constructor(apiController, docsController, options) {
        super(apiController, docsController, options);
    }
    doRequest(req, res) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                const requestObj = yield this.buildRequestObject(req);
                phLogger_1.default.info(requestObj);
                const responseObj = yield this.api.handle(requestObj, req, res);
                const hbs = JSON.parse(responseObj.body).data.attributes.hbs;
                const result = yield phS3Facade_1.default.getObject("ph-cli-dag-template", hbs);
                responseObj.body = result.toString();
                responseObj.headers = { "content-type": "text/x-handlebars-template" };
                return this.sendResponse(responseObj);
            }
            catch (err) {
                // This case should only occur if building a request object fails, as the
                // controller should catch any internal errors and always returns a response.
                return this.sendError(err, req); // , res, next)
            }
        });
    }
    sendResponse(responseObj) {
        return responseObj;
    }
    sendError(errors, req) {
        return __awaiter(this, void 0, void 0, function* () {
            const responseObj = yield API_1.default.responseFromError(errors, req.headers.accept);
            return responseObj;
        });
    }
}
exports.default = AWSHbsTemplateStrategy;
//# sourceMappingURL=awsLambdaTemplate.js.map