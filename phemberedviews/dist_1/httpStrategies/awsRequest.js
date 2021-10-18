"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const http_1 = require("http");
class AWSReq extends http_1.IncomingMessage {
    constructor(event) {
        super(null);
        this.aborted = false;
        // @ts-ignore
        this.httpVersion = event.requestContext.protocol.toString();
        if (this.httpVersion === undefined) {
            this.httpVersion = "HTTP/1.1";
        }
        this.httpVersionMajor = 1.1;
        this.httpVersionMinor = 1.1;
        this.connection = null;
        // @ts-ignore
        const hds = event.headers;
        this.headers = {
            "accept": hds.Accept,
            "content-length": hds.contentLength,
            "content-type": hds.contentType,
            "transfer-encoding": hds.tranferEncoding
        };
        // @ts-ignore
        this.rawHeaders = event.headers;
        // @ts-ignore
        this.method = event.httpMethod;
        // @ts-ignore
        this.url = event.path;
        this.protocol =
            this.httpVersion.substr(0, this.httpVersion.indexOf("/")).toLowerCase();
        this.host = hds.Host;
        // @ts-ignore
        this.params = event.pathParameters;
        // this.query = parse(event.queryStringParameters)
        this.query = {};
        this.pagination = {};
        // @ts-ignore
        if (event.body) {
            // @ts-ignore
            this.body = JSON.parse(event.body);
        }
        // @ts-ignore
        this.processQueryStringParameters(event.queryStringParameters);
    }
    processQueryStringParameters(queryStringParameters) {
        if (queryStringParameters) {
            // @ts-ignore
            if (queryStringParameters["page[offset]"] !== undefined) {
                // @ts-ignore
                this.pagination.offset = queryStringParameters["page[offset]"];
            }
            // @ts-ignore
            if (queryStringParameters["page[limit]"] !== undefined) {
                // @ts-ignore
                this.pagination.limit = queryStringParameters["page[limit]"];
            }
            // @ts-ignore
            if (this.pagination.offset !== undefined || this.pagination.limit !== undefined) {
                // @ts-ignore
                this.query.page = this.pagination;
            }
            // @ts-ignore
            if (queryStringParameters.filter !== undefined) {
                // @ts-ignore
                this.query.filter = queryStringParameters.filter;
            }
            // @ts-ignore
            if (queryStringParameters.sort !== undefined) {
                // @ts-ignore
                this.query.sort = queryStringParameters.sort;
            }
        }
    }
}
exports.default = AWSReq;
//# sourceMappingURL=awsRequest.js.map