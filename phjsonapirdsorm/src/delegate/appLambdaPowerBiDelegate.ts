import axios from "axios"
import adapter from "axios/lib/adapters/http"
import querystring from "querystring"
import AppLambdaDelegate from "./appLambdaDelegate"

export default class AppLambdaPowerBiDelegate extends AppLambdaDelegate {

    // @ts-ignore
    public async exec(event: Map<string, any>) {
        const partnerId = "2a606eef-e7e9-41a4-8b05-9e1a4942d602"
        // @ts-ignore
        const type = event.pathParameters.type
        // @ts-ignore
        const rid = event.queryStringParameters.rid
        // @ts-ignore
        const gid = event.queryStringParameters.gid

        if (type === "token") {
            const bpTokenUri = `https://login.chinacloudapi.cn/${partnerId}/oauth2/token`
            const embeddedUrl = `https://api.powerbi.cn/v1.0/myorg/groups/${gid}/reports/${rid}/GenerateToken`
            const res = await axios.post(bpTokenUri, querystring.stringify({
                grant_type: "client_credentials",
                resource: "https://analysis.chinacloudapi.cn/powerbi/api",
                client_id: "d05ed8c1-bb5d-4534-a7aa-1ffca7696a87",
                client_secret: "K0XsmQv.NX45~Zc1gU.19OWicrzE0BC~hU"
            }), { adapter })
            const access_token = res.data.access_token
            const embeddedToken = await axios.post(embeddedUrl,
                {accessLevel: "View", allowSaveAs: "true"},
                { headers: {
                    Authorization: `Bearer ${access_token}`
                }, adapter})
            delete embeddedToken.headers["odata-version"]
            delete embeddedToken.headers["access-control-expose-headers"]
            delete embeddedToken.headers["transfer-encoding"]
            delete embeddedToken.headers["home-cluster-uri"]
            delete embeddedToken.headers["request-redirected"]
            delete embeddedToken.headers.requestid
            delete embeddedToken.headers["odata-version"]
            delete embeddedToken.headers["x-frame-options"]
            delete embeddedToken.headers["x-content-type-options"]
            return {
                statusCode: embeddedToken.status,
                output: [
                    {
                        "content-type": "application/json",
                        "connection": "keep-alive"
                    },
                    JSON.stringify({token: embeddedToken.data.token, expiration: embeddedToken.data.expiration})
                ]
            }
        } else {
            return await super.exec(event)
        }
    }
}
