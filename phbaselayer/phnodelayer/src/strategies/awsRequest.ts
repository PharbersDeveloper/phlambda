import { IncomingMessage } from "http"
import phLogger from "../logger/PhLogger"

export default class AWSReq extends IncomingMessage {
    public protocol?: string
    public host?: string
    public params?: object
    public query?: object
    public pagination: object
    public body?: object
    public queryStr?: string

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
                accept: hds.Accept,
                "content-length": hds.contentLength,
                "content-type": hds.contentType,
                "transfer-encoding": hds.tranferEncoding,
            }
        } else {
            // @ts-ignore
            const buffer = Buffer.from(event.body)
            this.headers = {
                accept: hds.Accept,
                "content-length": String(buffer.length),
                "content-type": hds.contentTyp || hds["content-type"] || "application/vnd.api+json",
                "transfer-encoding": hds.tranferEncoding,
            }
        }

        // @ts-ignore
        this.rawHeaders = event.headers
        // @ts-ignore
        this.method = event.httpMethod
        this.protocol = this.httpVersion.substr(0, this.httpVersion.indexOf("/")).toLowerCase()
        this.host = hds.Host
        // @ts-ignore
        this.params = event.pathParameters
        this.query = {}
        this.pagination = {}

        // @ts-ignore
        const idsArr = event.multiValueQueryStringParameters ? event.multiValueQueryStringParameters["ids[]"] : []
        // @ts-ignore
        this.ids = idsArr && idsArr.length > 0 ? idsArr : []

        // @ts-ignore
        if (event.body) {
            try {
                // @ts-ignore
                this.body = JSON.parse(event.body)
            } catch (e) {
                // @ts-ignore
                if (event.body.includes("&") && this.method === "POST" && this.params.hasOwnProperty("edp") && this.params.edp === "token") {
                    const body = {}
                    // @ts-ignore
                    for (const item of event.body.split("&")) {
                        const obj = item.split("=")
                        // .replace(/_(\w)/g, (all: any, letter: any) => letter.toUpperCase())
                        body[obj[0]] = obj[1]
                    }
                    this.body = body
                } else {
                    // @ts-ignore
                    this.body = event.body
                }
            }
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

    private processQueryStringParameters(queryStringParameters: any) {
        if (queryStringParameters) {
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
