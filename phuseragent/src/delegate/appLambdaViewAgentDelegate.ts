import * as fs from "fs"
import Handlebars from "handlebars"
import phLogger from "../logger/phLogger"
import AppLambdaDelegate from "./appLambdaDelegate"

export default class AppLambdaViewAgentDelegate extends AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        const res = await super.exec(event)
        // @ts-ignore
        const clientId = event.queryStringParameters.client_id
        // @ts-ignore
        const redirectUri = event.queryStringParameters.redirect_uri
        // @ts-ignore
        const secret = event.queryStringParameters.client_secret
        const hbs =  fs.readFileSync("config/login.hbs")
        const client = await this.store.find("client", [clientId], {})
        // @ts-ignore
        res.headers = { "content-type": "text/x-handlebars-template" }
        if (client.payload.records.length === 1) {
            // TODO: 暂时注释掉，Lambda啥时候解决读取S3的问题再变成动态
            // const components = await this.store.find("component", client.payload.records[0].clientComponents, {})
            // if (components.payload.records.length === 1) {
            //     phLogger.info(components.payload.records[0].hbs)
            // }

            if (client.payload.records[0].secret !== secret) {
                // @ts-ignore
                res.output[1] = "<h1>Error</h1>"
            } else {
                const result = String(hbs).
                replace("{{client_id}}", clientId).
                replace("{{redirect_uri}}", redirectUri).
                replace("{{client_secret}}", secret)
                phLogger.info(result)
                // @ts-ignore
                res.output[1] = result
            }
        } else {
            // @ts-ignore
            res.output[1] = String(hbs)
        }
        return res
    }
}
