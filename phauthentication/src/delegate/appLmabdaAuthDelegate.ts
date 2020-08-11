import CryptoJS from "crypto-js"
import fortune from "fortune"
import {ServerResponse} from "http"
import moment from "moment"
import {
    errors2response, PhInvalidAuthGrant,
    PhInvalidClient, PhInvalidGrantType,
    PhInvalidParameters,
    PhInvalidPassword,
    PhNotFoundError
} from "../errors/pherrors"
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

    public redisStore: any

    public async prepare() {
        await super.prepare()
        const record = this.genTokenRecord()
        const adapter = this.genRedisAdapter()
        this.redisStore = fortune(record, {adapter})
        await this.redisStore.connect()
    }

    // @ts-ignore
    public async exec(event: Map<string, any>) {
        // const req = new AWSReq(event, undefined)
        // const response = new ServerResponse(req)
        return await this.authHandler(event)
    }

    protected genTokenRecord() {
        const filename = "../models/token.js"
        return require(filename).default
    }

    protected async authHandler(event: Map<string, any>) {
        // @ts-ignore
        const token = event.authorizationToken
        const result = await this.redisStore.find("access", null, { match: { token }})
        const records = result.payload.records
        // @ts-ignore
        const arnList = event.methodArn.split(":")
        const resourceList = arnList[5].split("/")
        if ( records.length === 0 ) {
            // @ts-ignore
            return this.generatePolicy("undefined", "Deny", event.methodArn)
        }
        const scopes = records[0].scope.split("|")
        if (scopes.length === 1 && scopes[0] === "*") {
            // @ts-ignore
            return this.generatePolicy(records[0].uid, "Allow", event.methodArn)
        }
        const auth = records[0].scope.split("#").map((item) => {
            const scope = item.split("|")
            return this.identify(resourceList, scope)
        })
        if (auth.includes(true)) {
            // @ts-ignore
            return this.generatePolicy(records[0].uid, "Allow", event.methodArn)
        } else {
            // @ts-ignore
            return this.generatePolicy(records[0].uid, "Deny", event.methodArn)
        }
    }

    protected identify(arnRes: string[], scopes: string[]) {
        // const agent = scopes[0]
        const resource = scopes[1]
        const permissions = scopes[2]
        const permissionsValues = this.conf.permissions.values
        phLogger.info("resource ==>", resource)
        phLogger.info("permissions ==>", permissions)
        function resourceFlag() {
            if (resource === "*") {
                return true
            }
            return resource.split("::").includes(arnRes[3])
        }
        function permissionFlag() {
            // R => Read   W => R + Update + Create   X => R + Delete   A => 所有权限
            if (permissions === "A") {
                return true
            }
            const pem = permissionsValues.map((item) => {
                if ( item[0] === "W" || item[0] === "X") {
                    const read = permissionsValues.find((p) => p[0] === "R").substr(1)
                    return permissionsValues.find((p) => p[0] === item[0]) + read
                } else {
                    return item
                }
            })
            return pem.find((item) => scopes[2] === item[0]).split("::").includes(arnRes[2])
        }
        return resourceFlag() && permissionFlag()
    }

    protected generatePolicy(principalId, effect, resource) {
        const authResponse = {}
        // @ts-ignore
        authResponse.principalId = principalId
        if (effect && resource) {
            // @ts-ignore
            const policyDocument = {}
            // @ts-ignore
            policyDocument.Version = "2012-10-17"
            // @ts-ignore
            policyDocument.Statement = []
            const statementOne = {}
            // @ts-ignore
            statementOne.Action = "execute-api:Invoke"
            // @ts-ignore
            statementOne.Effect = effect
            // @ts-ignore
            statementOne.Resource = resource
            // @ts-ignore
            policyDocument.Statement[0] = statementOne
            // @ts-ignore
            authResponse.policyDocument = policyDocument
        }
        return authResponse
    }
}
