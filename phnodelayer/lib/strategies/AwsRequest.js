"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const http_1 = require("http");
const PhLogger_1 = __importDefault(require("../logger/PhLogger"));
class AWSReq extends http_1.IncomingMessage {
    constructor(event, projectName) {
        // @ts-ignore
        super(event.body);
        this.aborted = false;
        // @ts-ignore
        this.httpVersion = event.requestContext.protocol.toString();
        if (this.httpVersion === undefined) {
            this.httpVersion = 'HTTP/1.1';
        }
        this.httpVersionMajor = 1.1;
        this.httpVersionMinor = 1.1;
        this.connection = null;
        // @ts-ignore
        const hds = event.headers;
        if (hds.contentLength) {
            this.headers = {
                accept: hds.Accept,
                'content-length': hds.contentLength,
                'content-type': hds.contentType,
                'transfer-encoding': hds.tranferEncoding,
            };
        }
        else {
            // @ts-ignore
            const buffer = Buffer.from(event.body);
            this.headers = {
                accept: hds.Accept,
                'content-length': String(buffer.length),
                'content-type': 'application/vnd.api+json',
                'transfer-encoding': hds.tranferEncoding,
            };
        }
        // @ts-ignore
        this.rawHeaders = event.headers;
        // @ts-ignore
        this.method = event.httpMethod;
        this.protocol = this.httpVersion.substr(0, this.httpVersion.indexOf('/')).toLowerCase();
        this.host = hds.Host;
        // @ts-ignore
        this.params = event.pathParameters;
        this.query = {};
        this.pagination = {};
        // @ts-ignore
        const idsArr = event.multiValueQueryStringParameters ? event.multiValueQueryStringParameters['ids[]'] : [];
        // @ts-ignore
        this.ids = idsArr && idsArr.length > 0 ? idsArr : [];
        // @ts-ignore
        if (event.body) {
            // @ts-ignore
            this.body = JSON.parse(event.body);
        }
        // @ts-ignore
        this.processQueryStringParameters(event.queryStringParameters);
        if (this.queryStr.length) {
            // @ts-ignore
            this.url = event.path.substr(event.path.indexOf(projectName) + projectName.length) + '?' + this.queryStr;
        }
        else {
            // @ts-ignore
            this.url = event.path.substr(event.path.indexOf(projectName) + projectName.length);
            PhLogger_1.default.info('url', this.url);
        }
    }
    processQueryStringParameters(queryStringParameters) {
        if (queryStringParameters) {
            const keys = Object.keys(queryStringParameters);
            let queryStr = '';
            keys.forEach((ele) => {
                queryStr += `${ele}=${queryStringParameters[ele]}&`;
                PhLogger_1.default.info(ele);
                // @ts-ignore
                this.query[ele] = queryStringParameters[ele];
            });
            this.queryStr = queryStr.slice(0, queryStr.length - 1);
        }
        else {
            this.queryStr = '';
        }
    }
}
exports.default = AWSReq;
