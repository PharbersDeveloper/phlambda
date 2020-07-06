import fortune from "fortune"
import fortuneHTTP from "fortune-http"
import jsonApiSerializer from "fortune-json-api"
import mongoAdapter from "fortune-mongodb"
import MySQLAdapter from "fortune-mysql"
import postgresAdapter from "fortune-postgres"
import * as fs from "fs"
import http, {ServerResponse} from "http"
import * as yaml from "js-yaml"
import {JsonConvert, ValueCheckingMode} from "json2typescript"
import {ServerConf} from "../configFactory/serverConf"
import phLogger from "../logger/phLogger"
// import AWSLambdaStrategy from "../httpStrategies/awsLambda"
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
    private conf: ServerConf

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

    public async exec(event: Map<string, any>) {
        const req = new AWSReq(event)
        const response = new ServerResponse(req)
        await this.listener(req, response)
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

    protected genMySQLAdapter() {
        const url = "mysql://root:Abcde196125@localhost/ph_offweb?debug=true&charset=BIG5_CHINESE_CI&timezone=+0800"
        return [MySQLAdapter , {
            url
        }]
    }

    protected genPgAdapter() {
        const url = "postgres://postgres:196125@localhost:5432/phoffweb"
        return [postgresAdapter , {
            url
        }]
    }

    protected genAdapter() {
        const prefix = this.conf.mongo.algorithm
        const host = this.conf.mongo.host
        const username = this.conf.mongo.username
        const pwd = this.conf.mongo.pwd
        const coll = this.conf.mongo.coll
        const url = prefix + "://" + username + ":" + pwd + "@" + host +  "/" + coll + "?retryWrites=true&w=majority"
        return [ mongoAdapter, {
            url,
            autoReconnect: true,
            keepAlive: true,
            keepAliveInitialDelay: 1000,
            useNewUrlParser: true
        } ]
    }
}
