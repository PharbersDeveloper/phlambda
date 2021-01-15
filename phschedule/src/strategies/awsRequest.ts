
import {IncomingHttpHeaders, IncomingMessage} from "http"
import phLogger from "../logger/phLogger"

export default class AWSReq extends IncomingMessage {
    public protocol?: string
    public host?: string
    public params?: object
    public query?: object
    public pagination: object
    public body ?: object
    public queryStr ?: string

    constructor(event: object, projectName: string) {
        // @ts-ignore
        super(event.body)
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
        if (hds.contentLength) {
            this.headers = {
                "accept": hds.Accept,
                "content-length": hds.contentLength,
                "content-type": hds.contentType,
                "transfer-encoding": hds.tranferEncoding
            }
        } else {
            // @ts-ignore
            const buffer = Buffer.from(event.body)
            this.headers = {
                "accept": hds.Accept,
                "content-length": String(buffer.length),
                "content-type": "application/vnd.api+json", // hds.contentType,
                "transfer-encoding": hds.tranferEncoding
            }
        }

        // @ts-ignore
        this.rawHeaders = event.headers
        // @ts-ignore
        this.method = event.httpMethod

        this.protocol =
            this.httpVersion.substr(0, this.httpVersion.indexOf("/")).toLowerCase()
        this.host = hds.Host
        // @ts-ignore
        this.params = event.pathParameters
        // this.query = parse(event.queryStringParameters)
        this.query = {}
        this.pagination = {}

        // @ts-ignore
        const idsArr = event.multiValueQueryStringParameters ? event.multiValueQueryStringParameters["ids[]"] : []
        // @ts-ignore
        this.ids = idsArr && idsArr.length > 0 ? idsArr : []

        // @ts-ignore
        if (event.body) {
            // @ts-ignore
            this.body = JSON.parse( event.body )
        }

        // @ts-ignore
        this.processQueryStringParameters(event.queryStringParameters)

        if (this.queryStr.length) {
            // @ts-ignore
            this.url = event.path.substr(event.path.indexOf(projectName) + projectName.length) + "?" + this.queryStr
        } else {
            // @ts-ignore
            this.url = event.path.substr(event.path.indexOf(projectName) + projectName.length)
            phLogger.info("url", this.url)
        }

    }

    private processQueryStringParameters(queryStringParameters: object) {
        if (queryStringParameters) {
            // // @ts-ignore
            // if (queryStringParameters["page[offset]"] !== undefined) {
            //     // @ts-ignore
            //     this.pagination.offset = queryStringParameters["page[offset]"]
            // }
            // // @ts-ignore
            // if (queryStringParameters["page[limit]"] !== undefined) {
            //     // @ts-ignore
            //     this.pagination.limit = queryStringParameters["page[limit]"]
            // }
            // // @ts-ignore
            // if (this.pagination.offset !== undefined || this.pagination.limit !== undefined) {
            //     // @ts-ignore
            //     this.query.page = this.pagination
            // }
            // // @ts-ignore
            // // if (queryStringParameters.filter !== undefined) {
            // //     // @ts-ignore
            // //     this.query.filter = queryStringParameters.filter
            // // }
            // // @ts-ignore
            // if (queryStringParameters.sort !== undefined) {
            //     // @ts-ignore
            //     this.query.sort = queryStringParameters.sort
            // }

            const keys = Object.keys(queryStringParameters)
            let queryStr = ""
            keys.forEach((ele) => {
                queryStr += `${ele}=${queryStringParameters[ele]}&`
                phLogger.info(ele)
                // @ts-ignore
                this.query[ele] = queryStringParameters[ele]
            })

            this.queryStr = queryStr.slice(0, queryStr.length - 1)

        } else {
            this.queryStr = ""
        }
    }
}