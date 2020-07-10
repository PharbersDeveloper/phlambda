import fortune from "fortune"
import jsonApiSerializer from "fortune-json-api"
// import mongoAdapter from "fortune-mongodb"
// import MySQLAdapter from "fortune-mysql"
import postgresAdapter from "fortune-postgres"
import * as fs from "fs"
import http, {ServerResponse} from "http"
import * as yaml from "js-yaml"
import {JsonConvert, ValueCheckingMode} from "json2typescript"
import fortuneHTTP from "../../lib/fortune-http"
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
    // private httpStrategies: AWSLambdaStrategy
    public store: any
    public listener: any
    protected conf: ServerConf

    public prepare() {
        this.loadConfiguration()
        const record = this.genRecord()
        const adapter = this.genPgAdapter()
        this.store = fortune(record, {adapter})
        // await this.store.connect()
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
        // @ts-ignore
        if ( !event.body ) {
            // @ts-ignore
            event.body = ""
        }
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
            // jsonConvert.operationMode = OperationMode.LOGGING // print some debug data
            jsonConvert.ignorePrimitiveChecks = false // don't allow assigning number to string etc.
            jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
            this.conf = jsonConvert.deserializeObject(doc, ServerConf)
            // this.exportHandler = new ExportProejct(this.conf.oss)
            // this.kafka = new KafkaDelegate(this.conf.kfk)
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
}