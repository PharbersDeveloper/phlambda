"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs = __importStar(require("fs"));
const yaml = __importStar(require("js-yaml"));
const json_api_1 = __importDefault(require("json-api"));
const json2typescript_1 = require("json2typescript");
const mongoose = require("mongoose");
const serverConf_1 = require("../configFactory/serverConf");
const awsLambda_1 = __importDefault(require("../httpStrategies/awsLambda"));
const awsRequest_1 = __importDefault(require("../httpStrategies/awsRequest"));
const phLogger_1 = __importDefault(require("../logger/phLogger"));
const urlEncodeFilterParser_1 = require("./urlEncodeFilterParser");
/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */
class AppLambdaDelegate {
    prepare() {
        this.loadConfiguration();
        this.connect2MongoDB();
        this.generateRoutes(this.getModelRegistry());
    }
    exec(event) {
        return __awaiter(this, void 0, void 0, function* () {
            if (mongoose.connection.readyState !== 1) {
                this.connect2MongoDB();
            }
            const req = new awsRequest_1.default(event);
            // @ts-ignore
            return yield this.httpStrategies.doRequest(req, null);
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
    connect2MongoDB() {
        const prefix = this.conf.mongo.algorithm;
        const host = this.conf.mongo.host;
        const port = `${this.conf.mongo.port}`;
        const username = this.conf.mongo.username;
        const pwd = this.conf.mongo.pwd;
        const coll = this.conf.mongo.coll;
        const auth = this.conf.mongo.auth;
        const authSource = this.conf.mongo.authSource;
        if (auth) {
            phLogger_1.default.info(`connect mongodb with ${username} and ${pwd}`);
            mongoose.connect(prefix + "://" + username + ":" + pwd + "@" + host + ":" + port + "/" + coll + "?authSource=" + authSource, (err) => {
                if (err != null) {
                    phLogger_1.default.error(err);
                }
            });
        }
        else {
            phLogger_1.default.info(`connect mongodb without auth`);
            mongoose.connect(prefix + "://" + host + ":" + port + "/" + coll, { useNewUrlParser: true, autoReconnect: true }, (err) => {
                if (err != null) {
                    phLogger_1.default.error(err);
                }
            });
        }
    }
    getModelRegistry() {
        const result = {};
        this.conf.models.forEach((ele) => {
            result[ele.reg] = {};
        });
        return new json_api_1.default.ResourceTypeRegistry(result, {
            dbAdapter: new json_api_1.default.dbAdapters.Mongoose(this.generateModels()),
            info: {
                description: "Blackmirror inc. Alfred Yang 2019"
            },
            urlTemplates: {
                self: "/{type}/{id}"
            },
        });
    }
    generateModels() {
        const path = "../models/" + this.conf.project + "/";
        const suffix = ".js";
        const result = {};
        this.conf.models.forEach((ele) => {
            const filename = path + ele.file + suffix;
            const one = require(filename).default;
            result[ele.file] = new one().getModel();
        });
        return result;
    }
    generateRoutes(registry) {
        const opts = {
            filterParser: urlEncodeFilterParser_1.urlEncodeFilterParser
        };
        this.httpStrategies = new awsLambda_1.default(new json_api_1.default.controllers.API(registry, opts), new json_api_1.default.controllers.Documentation(registry, { name: "Pharbers API" }));
    }
}
exports.default = AppLambdaDelegate;
//# sourceMappingURL=appLambdaDelegate.js.map