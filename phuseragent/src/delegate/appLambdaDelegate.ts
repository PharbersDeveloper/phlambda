import * as fs from "fs"
import { ServerResponse } from "http"
import { AWSRequest, dbFactory, store } from "phnodelayer"
import {
    errors2response,
    PhInvalidClient,
    PhInvalidParameters,
} from "../errors/pherrors"

export default class AppLambdaDelegate {
    public dbIns: any = dbFactory.getInstance.getStore(store.Postgres)
    public async exec(event: Map<string, any>) {
        await this.dbIns.connect()
        try {
            const req = new AWSRequest(event, "common")
            const response = new ServerResponse(req)
            // @ts-ignore
            const clientId = event.queryStringParameters.client_id
            // @ts-ignore
            const redirectUri = event.queryStringParameters.redirect_uri
            // @ts-ignore
            const secret = event.queryStringParameters.client_secret
            const hbs =  fs.readFileSync("config/login.hbs")
            const client = await this.dbIns.find("client", [clientId], {})
            if (client.payload.records.length === 0) {
                errors2response(PhInvalidClient, response)
                return response
            }

            if (client.payload.records[0].secret !== secret) {
                errors2response(PhInvalidParameters, response)
                return response
            }

            if (redirectUri === "" || redirectUri === undefined) {
                errors2response(PhInvalidParameters, response)
                return response
            }
            // @ts-ignore
            response.headers = { "Content-Type": "text/x-handlebars-template" }
            const result = String(hbs).
            replace("{{client_id}}", clientId).
            replace("{{redirect_uri}}", redirectUri).
            replace("{{client_secret}}", secret)
            response.statusCode = 200
            // @ts-ignore
            response.body = result
            return response
        } catch (e) {
            throw e
        } finally {
            await this.dbIns.disconnect()
        }
    }
}
