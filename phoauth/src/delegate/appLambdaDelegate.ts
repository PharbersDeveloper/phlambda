import fortune from "fortune"
import fortuneHTTP from "fortune-http"
import jsonApiSerializer from "fortune-json-api"
import postgresAdapter from "fortune-postgres"
import redisAdapter from "fortune-redis"
import * as fs from "fs"
import {ServerResponse} from "http"
import * as yaml from "js-yaml"
import {JsonConvert, ValueCheckingMode} from "json2typescript"
import {ServerConf} from "../configFactory/serverConf"
import phLogger from "../logger/phLogger"
import AWSReq from "../strategies/awsRequest"

/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */
export default class AppLambdaDelegate {
    public store: any
    public listener: any
    public isFirstInit = true
    protected conf: ServerConf

    public async prepare() {
        this.loadConfiguration()
        const record = this.genRecord()
        const adapter = this.genPgAdapter()
        this.store = fortune(record, {adapter})
        await this.store.connect()
        this.isFirstInit = false
        this.listener = fortuneHTTP(this.store, {
            serializers: [
                [ jsonApiSerializer ]
            ]
        })
    }

    public async cleanUp() {
        await this.store.disconnect()
    }

    public async exec(event: Map<string, any>) {
        const req = new AWSReq(event, this.conf.project)
        const response = new ServerResponse(req)
        // @ts-ignore
        const buffer = Buffer.from(event.body)
        // @ts-ignore
        req._readableState.buffer = buffer
        await this.listener(req, response, buffer)
        return response
    }

    protected loadConfiguration() {
        try {
            const path = "config/server.yml"
            const jsonConvert = new JsonConvert()
            const doc = yaml.safeLoad(fs.readFileSync(path, "utf8"))
            jsonConvert.ignorePrimitiveChecks = false // don't allow assigning number to string etc.
            jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
            this.conf = jsonConvert.deserializeObject(doc, ServerConf)

        } catch (e) {
            phLogger.fatal( e as Error )
        }
    }

    protected genRecord() {
        const filename = "../models/" + this.conf.project + ".js"
        return require(filename).default
    }

    protected genPgAdapter() {
        const prefix = this.conf.postgres.algorithm
        const host = this.conf.postgres.host
        const port = this.conf.postgres.port
        const username = this.conf.postgres.username
        const pwd = this.conf.postgres.pwd
        const dbName = this.conf.postgres.dbName
        const url = prefix + "://" + username + ":" + pwd + "@" + host + ":" + port + "/" + dbName
        // const url = "postgres://postgres:196125@localhost:5432/phoffweb"
        return [postgresAdapter , {
            url
        }]
    }

    protected genRedisAdapter() {
        const prefix = this.conf.redis.algorithm
        const host = this.conf.redis.host
        const port = this.conf.redis.port
        const db = this.conf.redis.db
        const url = `${prefix}://${host}:${port}/${db}`
        return [redisAdapter , {
            url
        }]
    }
}
