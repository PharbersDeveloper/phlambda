import axios from "axios"
import adapter from "axios/lib/adapters/http"
import querystring from "querystring"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        // @ts-ignore
        const type = event.pathParameters.type
        // @ts-ignore
        const rid = event.queryStringParameters.rid
        // @ts-ignore
        const gid = event.queryStringParameters.gid

        if (type === "token") {
            const powerBIURI = process.env.POWERBIURI.replace("{partnerId}", process.env.PARTNERID)
            const embeddedRI = process.env.EMBEDDEDURI.replace("{gid}", gid).replace("{rid}", rid)
            const resource = process.env.RESOURCE
            const clientId = process.env.CLIENTID
            const clientSecret = process.env.CLIENTSECRET

            const res = await axios.post(powerBIURI, querystring.stringify({
                grant_type: "client_credentials",
                resource,
                client_id: clientId,
                client_secret: clientSecret
            }), {adapter})
            const access_token = res.data.access_token
            const embeddedToken = await axios.post(embeddedRI,
                {accessLevel: "View", allowSaveAs: "true"},
                {
                    headers: {
                        Authorization: `Bearer ${access_token}`
                    }, adapter
                })
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
        }
    }
}
