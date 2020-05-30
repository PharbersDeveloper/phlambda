import * as fs from "fs"
import * as yaml from "js-yaml"
import {ServerConf} from "../configFactory/serverConf"
import phLogger from "../logger/phLogger"

import j2t = require("json2typescript")
const JsonConvert = j2t.JsonConvert
const ValueCheckingMode = j2t.ValueCheckingMode

/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */
export default class AppLambdaDelegate {

    private conf: ServerConf

    public prepare() {
        this.loadConfiguration()
        phLogger.info(this.conf)
    }

    public exec(event: Map<string, any>) {
        phLogger.info(event)
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
}
