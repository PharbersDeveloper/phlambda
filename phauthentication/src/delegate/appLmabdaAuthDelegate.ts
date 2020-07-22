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
        const response = {}
        await this.authHandler(event, response)
        return response
    }

    protected genTokenRecord() {
        const filename = "../models/token.js"
        return require(filename).default
    }

    protected async authHandler(event: Map<string, any>, response: object) {
        // @ts-ignore
        const token = event.authorizationToken
        const result = await this.redisStore.find("access", null, { match: { token }})
        const records = result.payload.records
        if ( records.length === 0 ) {
            return response
        }
        const uid = records[0].uid
        const role = await this.store.find("role", null, { match: { accountRole: uid }})
        const scope = await this.store.find("scope", null, { match: { owner: role.payload.records[0].id }})
        const policy = scope.payload.records[0].scopePolicy
        phLogger.info(policy)
        return response
    }
}
