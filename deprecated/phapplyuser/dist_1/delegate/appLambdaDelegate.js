"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const fortune_1 = __importDefault(require("fortune"));
// import mongoAdapter from "fortune-mongodb"
// import MySQLAdapter from "fortune-mysql"
const fortune_postgres_1 = __importDefault(require("fortune-postgres"));
const fs = __importStar(require("fs"));
const http_1 = require("http");
const yaml = __importStar(require("js-yaml"));
const json2typescript_1 = require("json2typescript");
const fortune_http_1 = __importDefault(require("../../lib/fortune-http"));
const fortune_json_api_1 = __importDefault(require("../../lib/fortune-json-api"));
const serverConf_1 = require("../configFactory/serverConf");
const phLogger_1 = __importDefault(require("../logger/phLogger"));
const awsRequest_1 = __importDefault(require("../strategies/awsRequest"));
/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */
class AppLambdaDelegate {
    constructor() {
        this.isFirstInit = true;
        // protected genAdapter() {
        //     const prefix = this.conf.mongo.algorithm
        //     const host = this.conf.mongo.host
        //     const username = this.conf.mongo.username
        //     const pwd = this.conf.mongo.pwd
        //     const coll = this.conf.mongo.coll
        //     const url = prefix + "://" + username + ":" + pwd + "@" + host +  "/" + coll + "?retryWrites=true&w=majority"
        //     return [ mongoAdapter, {
        //         url,
        //         autoReconnect: true,
        //         keepAlive: true,
        //         keepAliveInitialDelay: 1000,
        //         useNewUrlParser: true
        //     } ]
        // }
    }
    prepare() {
        return __awaiter(this, void 0, void 0, function* () {
            this.loadConfiguration();
            const record = this.genRecord();
            const adapter = this.genPgAdapter();
            this.store = fortune_1.default(record, { adapter });
            yield this.store.connect();
            this.isFirstInit = false;
            this.listener = fortune_http_1.default(this.store, {
                serializers: [
                    [fortune_json_api_1.default]
                ]
            });
        });
    }
    cleanUp() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.store.disconnect();
        });
    }
    exec(event) {
        return __awaiter(this, void 0, void 0, function* () {
            // @ts-ignore
            if (!event.body) {
                // @ts-ignore
                event.body = "";
            }
            const req = new awsRequest_1.default(event, this.conf.project);
            const response = new http_1.ServerResponse(req);
            // @ts-ignore
            const buffer = Buffer.from(event.body);
            // @ts-ignore
            req._readableState.buffer = buffer;
            yield this.listener(req, response, buffer);
            return response;
        });
    }
    loadConfiguration() {
        try {
            const path = "config/server.yml";
            const jsonConvert = new json2typescript_1.JsonConvert();
            const doc = yaml.safeLoad(fs.readFileSync(path, "utf8"));
            // jsonConvert.operationMode = OperationMode.LOGGING // print some debug data
            jsonConvert.ignorePrimitiveChecks = false; // don't allow assigning number to string etc.
            jsonConvert.valueCheckingMode = json2typescript_1.ValueCheckingMode.DISALLOW_NULL; // never allow null
            this.conf = jsonConvert.deserializeObject(doc, serverConf_1.ServerConf);
            // this.exportHandler = new ExportProejct(this.conf.oss)
            // this.kafka = new KafkaDelegate(this.conf.kfk)
        }
        catch (e) {
            phLogger_1.default.fatal(e);
        }
    }
    genRecord() {
        const filename = "../models/" + this.conf.project + ".js";
        return require(filename).default;
    }
    // protected genMySQLAdapter() {
    //     const url = "mysql://root:Abcde196125@localhost/ph_offweb?debug=true&charset=BIG5_CHINESE_CI&timezone=+0800"
    //     return [MySQLAdapter , {
    //         url
    //     }]
    // }
    genPgAdapter() {
        const prefix = this.conf.postgres.algorithm;
        const host = this.conf.postgres.host;
        const port = this.conf.postgres.port;
        const username = this.conf.postgres.username;
        const pwd = this.conf.postgres.pwd;
        const dbName = this.conf.postgres.dbName;
        const url = prefix + "://" + username + ":" + pwd + "@" + host + ":" + port + "/" + dbName;
        // const url = "postgres://postgres:196125@localhost:5432/phoffweb"
        return [fortune_postgres_1.default, {
                url
            }];
    }
}
exports.default = AppLambdaDelegate;
//# sourceMappingURL=appLambdaDelegate.js.map