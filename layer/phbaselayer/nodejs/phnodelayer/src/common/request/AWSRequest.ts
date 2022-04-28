
import PhLogger from "../logger/phLogger"
import {IncomingMessage} from "http"

export default class AWSRequest extends IncomingMessage {
    public protocol?: string
    public host?: string
    public params?: any
    public query?: any
    public pagination: any
    public body?: any
    public queryStr?: string
    public ids: any[]

    constructor(event: any, projectName: string) {
        super(event.body)
        this.aborted = false
        this.httpVersion = event.requestContext.protocol.toString()
        if (this.httpVersion === undefined) {
            this.httpVersion = "HTTP/1.1"
        }
        this.httpVersionMajor = 1.1
        this.httpVersionMinor = 1.1
        // this.connection = null
        const hds = event.headers
        if (hds.contentLength) {
            this.headers = {
                accept: hds.Accept,
                "content-length": hds.contentLength,
                "content-type": hds.contentType,
                "transfer-encoding": hds.tranferEncoding,
            }
        } else {
            const buffer = Buffer.from(event.body)
            this.headers = {
                accept: hds.Accept,
                "content-length": String(buffer.length),
                "content-type": hds.contentTyp || hds["content-type"] || "application/vnd.api+json",
                "transfer-encoding": hds.tranferEncoding,
            }
        }

        this.rawHeaders = event.headers
        this.method = event.httpMethod
        this.protocol = this.httpVersion.substr(0, this.httpVersion.indexOf("/")).toLowerCase()
        this.host = hds.Host
        this.params = event.pathParameters
        this.query = {}
        this.pagination = {}

        const idsArr = event.multiValueQueryStringParameters ? event.multiValueQueryStringParameters["ids[]"] : []
        this.ids = idsArr && idsArr.length > 0 ? idsArr : []

        if (event.body) {
            try {
                this.body = JSON.parse(event.body)
            } catch (e) {
                if (event.body.includes("&") && this.method === "POST" && this.params.hasOwnProperty("edp") && this.params.edp === "token") {
                    const body = {}
                    for (const item of event.body.split("&")) {
                        const obj = item.split("=")
                        // .replace(/_(\w)/g, (all: any, letter: any) => letter.toUpperCase())
                        body[obj[0]] = obj[1]
                    }
                    this.body = body
                } else {
                    this.body = event.body
                }
            }
        }

        this.processQueryStringParameters(event.queryStringParameters)

        if (this.queryStr.length) {
            this.url = event.path.substr(event.path.indexOf(projectName) + projectName.length) + "?" + this.queryStr
        } else {
            this.url = event.path.substr(event.path.indexOf(projectName) + projectName.length)
            PhLogger.info("url", this.url)
        }

    }

    private processQueryStringParameters(queryStringParameters: any) {
        if (queryStringParameters) {
            const keys = Object.keys(queryStringParameters)
            let queryStr = ""
            keys.forEach((ele) => {
                queryStr += `${ele}=${queryStringParameters[ele]}&`
                PhLogger.info(ele)
                this.query[ele] = queryStringParameters[ele]
            })
            this.queryStr = queryStr.slice(0, queryStr.length - 1)
        } else {
            this.queryStr = ""
        }
    }
}
