import fortune from "fortune"
import fortuneHTTP from "fortune-http"
import jsonApiSerializer from "fortune-json-api"
import postgresAdapter from "fortune-postgres"
import * as fs from "fs"
import * as yaml from "js-yaml"
import {JsonConvert, ValueCheckingMode} from "json2typescript"
import mongoose = require("mongoose")
import {ServerConf} from "../configFactory/serverConf"
import mongo2postgres from "../dataExchange/mongo2postgres"
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

        this.connect2Mongodb()
    }

    public async exec(event: Map<string, any>) {
        return await mongo2postgres(mongoose, this.store)
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

    // protected genMySQLAdapter() {
    //     const url = "mysql://root:Abcde196125@localhost/ph_offweb?debug=true&charset=BIG5_CHINESE_CI&timezone=+0800"
    //     return [MySQLAdapter , {
    //         url
    //     }]
    // }

    protected genPgAdapter() {
        const prefix = this.conf.postgres.algorithm
        const host = this.conf.postgres.host
        const port = this.conf.postgres.port
        const username = this.conf.postgres.username
        const pwd = this.conf.postgres.pwd
        const dbName = this.conf.postgres.dbName
        const url = prefix + "://" + username + ":" + pwd + "@" + host + ":" + port + "/" + dbName
        return [postgresAdapter , {
            url
        }]
    }

    protected connect2Mongodb() {
        const prefix = this.conf.mongo.algorithm
        const host = this.conf.mongo.host
        const port = this.conf.mongo.port
        const username = this.conf.mongo.username
        const pwd = this.conf.mongo.pwd
        const coll = this.conf.mongo.coll
        // const url = prefix + "://" + username + ":" + pwd + "@" + host +  "/" + coll + "?retryWrites=true&w=majority"
        mongoose.connect(prefix + "://" + username + ":" + pwd + "@" + host + ":" + port + "/" + coll + "?authSource=admin",
            { useNewUrlParser: true, autoReconnect: true, keepAlive: true, keepAliveInitialDelay: 1000 },
            (err: any) => {
                if (err != null) {
                    phLogger.error(err)
                }
            })
    }
}
