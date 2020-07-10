import {ServerResponse} from "http"
import phLogger from "../logger/phLogger"
import AWSReq from "../strategies/awsRequest"
import AppLambdaDelegate from "./appLambdaDelegate"

/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */
export default class AppLambdaAuthDelegate extends AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        const req = new AWSReq(event, undefined)
        const response = new ServerResponse(req)
        // @ts-ignore
        const endpoint = event.pathParameters.edp
        if (endpoint === "login") {
            await this.loginHandler(event, response)
        }
        return response
    }

    protected async loginHandler(event: Map<string, any>, response: ServerResponse) {
        // @ts-ignore
        const body = JSON.parse(event.body)
        const email = body.email
        const pwd = body.password
        // @ts-ignore
        const result = await this.store.find("account", null, { match: { email } } )
        // const response = {}
        if (result.payload.records.length === 0) {
            // @ts-ignore
            response.statusCode = 404
            // @ts-ignore
            response.headers = { "Content-Type": "application/json", "Accept": "application/json" }
            // @ts-ignore
            response.body = "User Not Found"
        } else if (result.payload.records.length === 1) {

            const account = result.payload.records[0]
            phLogger.info(account)

            if (account.password === body.password) {
                // @ts-ignore
                response.statusCode = 200
                // @ts-ignore
                response.headers = { "Content-Type": "application/json", "Accept": "application/json" }
                // @ts-ignore
                response.body = result.payload.records[0]
            } else {
                // @ts-ignore
                response.statusCode = 403
                // @ts-ignore
                response.headers = { "Content-Type": "application/json", "Accept": "application/json" }
                // @ts-ignore
                response.body = "wrong password"
            }

        } else {
            // @ts-ignore
            response.statusCode = 500
            // @ts-ignore
            response.headers = { "Content-Type": "application/json", "Accept": "application/json" }
            // @ts-ignore
            response.body = ""
        }

        phLogger.info(response)
        return response
    }
}
