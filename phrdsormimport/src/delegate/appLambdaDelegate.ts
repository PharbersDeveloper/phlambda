import fortune from "fortune"
import mongoAdapter from "fortune-mongodb"
import MySQLAdapter from "fortune-mysql"
import * as fs from "fs"
import * as yaml from "js-yaml"
import {JsonConvert, ValueCheckingMode} from "json2typescript"
import {ServerConf} from "../configFactory/serverConf"
// import AWSLambdaStrategy from "../httpStrategies/awsLambda"
// import AWSReq from "../httpStrategies/awsRequest"
import phLogger from "../logger/phLogger"

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

    private conf: ServerConf

    public async prepare() {
        this.loadConfiguration()
        const record = this.genRecord()
        const adapter = this.genMySQLAdapter()
        this.store = fortune(record, {adapter})
        await this.store.connect()
    }

    public async exec(event: Map<string, any>) {
        // const req = new AWSReq(event)
        // @ts-ignore
        return await this.httpStrategies.doRequest(req, null)
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
