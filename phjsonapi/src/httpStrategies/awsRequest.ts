
import { parse, stringify } from "@billjs/query-string"
import {IncomingHttpHeaders, IncomingMessage} from "http"
import phLogger from "../logger/phLogger"

export default class AWSReq extends IncomingMessage {
    public protocol?: string
    public host?: string
    public params?: object
    public query?: object
    public pagination: object

    constructor(event: object) {
        super(null)
        this.aborted = false
        // @ts-ignore
        this.httpVersion = event.requestContext.protocol.toString()
        if (this.httpVersion === undefined) {
            this.httpVersion = "HTTP/1.1"
        }
        this.httpVersionMajor = 1.1
        this.httpVersionMinor = 1.1
        this.connection = null
        // @ts-ignore
        const hds = event.headers
        this.headers = {
            "accept": hds.Accept,
            "content-length": hds.contentLength,
            "content-type": hds.contentType,
            "transfer-encoding": hds.tranferEncoding
        }
        // @ts-ignore
        this.rawHeaders = event.headers
        // @ts-ignore
        this.method = event.httpMethod
        // @ts-ignore
        this.url = event.path
        this.protocol =
            this.httpVersion.substr(0, this.httpVersion.indexOf("/")).toLowerCase()
        this.host = hds.Host
        // @ts-ignore
        this.params = event.pathParameters
        // this.query = parse(event.queryStringParameters)
        this.query = {}
        this.pagination = {}
        // @ts-ignore
        if (event.queryStringParameters["page[offset]"] !== undefined) {
            // @ts-ignore
            this.pagination.offset = event.queryStringParameters["page[offset]"]
        }
        // @ts-ignore
        if (event.queryStringParameters["page[limit]"] !== undefined) {
            // @ts-ignore
            this.pagination.limit = event.queryStringParameters["page[limit]"]
        }
        // @ts-ignore
        if (this.pagination.offset !== undefined || this.pagination.limit !== undefined) {
            // @ts-ignore
            this.query.page = this.pagination
        }
    }
}
