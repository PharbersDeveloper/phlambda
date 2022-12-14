import typeIs from "type-is"
import { InvalidArgumentError } from "./errors"
import { hasOwnProperty } from "./utils/fn"

export class Request {
    body: any
    headers: any
    method: any
    query: any
    constructor(options: any = {}) {
        if (!options.headers) {
            throw new InvalidArgumentError("Missing parameter: `headers`")
        }

        if (!options.method) {
            throw new InvalidArgumentError("Missing parameter: `method`")
        }

        if (!options.query) {
            throw new InvalidArgumentError("Missing parameter: `query`")
        }

        this.body = options.body || {}
        this.headers = {}
        this.method = options.method
        this.query = options.query

        // Store the headers in lower case.
        // tslint:disable-next-line:forin
        for (const field in options.rawHeaders) {
            this.headers[field.toLowerCase()] = options.rawHeaders[field]
            // if (hasOwnProperty(options.headers, field)) {
            //     this.headers[field.toLowerCase()] = options.rawHeaders[field]
            // }
        }

        // Store additional properties of the request object passed in
        for (const property in options) {
            if (hasOwnProperty(options, property) && !this[property]) {
                this[property] = options[property]
            }
        }
    }

    /**
     * Get a request header.
     */

    get(field: string) {
        return this.headers[field.toLowerCase()]
    }

    /**
     * Check if the content-type matches any of the given mime type.
     */
    is(args: string[]): string | false
    is(...args: string[]): string | false

    is(...args) {
        let types = args
        if (Array.isArray(types[0])) {
            types = types[0]
        }

        return typeIs.is(this as any, types) || false
    }
}
