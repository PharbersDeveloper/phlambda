import * as fs from "fs"
import * as yaml from "js-yaml"
import API, {ResourceTypeRegistry} from "json-api"
import {APIControllerOpts} from "json-api/build/src/controllers/API"
import ExpressStrategy from "json-api/build/src/http-strategies/Express"
import {JsonConvert, ValueCheckingMode} from "json2typescript"
import mongoose = require("mongoose")
import {ServerConf} from "../configFactory/serverConf"
import { default as ExcelDataInputOffweb } from "../exportProject/excelDataInputOffweb"
import AWSLambdaStrategy from "../httpStrategies/awsLambda"
import AWSReq from "../httpStrategies/awsRequest"
import phLogger from "../logger/phLogger"
import {urlEncodeFilterParser} from "./urlEncodeFilterParser"
/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */
export default class AppLambdaDelegate {

    private conf: ServerConf
    private httpStrategies: AWSLambdaStrategy

    public prepare() {
        this.loadConfiguration()
        this.connect2MongoDB()
        this.generateRoutes(this.getModelRegistry())
    }

    public checkMongoConnection() {
        return mongoose.connection.readyState === 1
    }

    public async exec(event: Map<string, any>) {
        if (mongoose.connection.readyState !== 1) {
            this.connect2MongoDB()
        }
        const req = new AWSReq(event)
        // @ts-ignore
        return await this.httpStrategies.doRequest(req, null)
    }

    public async excelImportData(event: Map<string, any>) {
        if (!this.checkMongoConnection()) {
            this.connect2MongoDB()
        }
        const importData = new ExcelDataInputOffweb(event)

        return await importData.excelModelData()
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

    protected connect2MongoDB() {
        const prefix = this.conf.mongo.algorithm
        const host = this.conf.mongo.host
        const port = `${this.conf.mongo.port}`
        const username = this.conf.mongo.username
        const pwd = this.conf.mongo.pwd
        const coll = this.conf.mongo.coll
        const auth = this.conf.mongo.auth
        const authSource = this.conf.mongo.authSource
        if (auth) {
            phLogger.info(`connect mongodb with ${ username } and ${ pwd }`)
            mongoose.connect(prefix + "://" + username + ":" + pwd + "@" + host + ":" + port + "/" + coll + "?authSource=" + authSource,
                { useNewUrlParser: true, autoReconnect: true },
                (err: any) => {
                    if (err != null) {
                        phLogger.error(err)
                    }
                })
        } else {
            phLogger.info(`connect mongodb without auth`)
            mongoose.connect(prefix + "://" + host + ":" + port + "/" + coll,
                { useNewUrlParser: true, autoReconnect: true },
                (err: any) => {
                    if (err != null) {
                        phLogger.error(err)
                    }
            })
        }
    }

    protected getModelRegistry(): ResourceTypeRegistry {
        const result: {[index: string]: any} = {}
        this.conf.models.forEach((ele) => {
            result[ele.reg] = {}
        })
        return new API.ResourceTypeRegistry(result, {
            dbAdapter: new API.dbAdapters.Mongoose(this.generateModels()),
            info: {
                description: "Blackmirror inc. Alfred Yang 2019"
            },
            urlTemplates: {
                self: "/{type}/{id}"
            },
        })
    }

    protected generateModels(): any {
        const path = "../models/" + this.conf.project + "/"
        const suffix = ".js"
        const result: {[index: string]: any} = {}
        this.conf.models.forEach((ele) => {
            const filename = path + ele.file + suffix
            const one = require(filename).default
            result[ele.file] = new one().getModel()
        })
        return result
    }

    protected generateRoutes(registry: ResourceTypeRegistry) {

        const opts: APIControllerOpts = {
            filterParser: urlEncodeFilterParser
        }

        this.httpStrategies = new AWSLambdaStrategy(
            new API.controllers.API(registry, opts),
            new API.controllers.Documentation(registry, {name: "Pharbers API"})
        )
    }
}
