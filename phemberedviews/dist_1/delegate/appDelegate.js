"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const axios_1 = __importDefault(require("axios"));
const body_parser_1 = __importDefault(require("body-parser"));
const express_1 = __importDefault(require("express"));
const fs = __importStar(require("fs"));
const yaml = __importStar(require("js-yaml"));
const json_api_1 = __importDefault(require("json-api"));
const json2typescript_1 = require("json2typescript");
const mongoose = require("mongoose");
const serverConf_1 = require("../configFactory/serverConf");
const ExportProject_1 = __importDefault(require("../exportProject/ExportProject"));
const KafkaDelegate_1 = __importDefault(require("../kafka/KafkaDelegate"));
const phLogger_1 = __importDefault(require("../logger/phLogger"));
const urlEncodeFilterParser_1 = require("./urlEncodeFilterParser");
/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */
class AppDelegate {
    constructor() {
        this.app = express_1.default();
        this.router = express_1.default.Router();
        this.exportHandler = null;
        this.kafka = null; // new KafkaDelegate()
    }
    /**
     * @returns the configuration of the server
     */
    get Conf() {
        return this.conf;
    }
    exec() {
        this.loadConfiguration();
        this.configMiddleware();
        this.connect2MongoDB();
        this.generateRoutes(this.getModelRegistry());
        this.listen2Port(8080);
    }
    uuidv4() {
        return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
            const r = Math.random() * 16 | 0;
            const v = c === "x" ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
    configMiddleware() {
        this.app.use(body_parser_1.default.json());
        this.app.use(body_parser_1.default.urlencoded({
            extended: true
        }));
        // a middleware function with no mount path. This code is executed for every request to the router
        this.router.use((req, res, next) => {
            const auth = req.get("Authorization");
            if (auth === undefined) {
                phLogger_1.default.error("no auth");
                res.status(500).send({ error: "no auth!" });
                return;
            }
            const host = this.conf.env.oauthHost;
            const port = this.conf.env.oauthPort;
            const namespace = this.conf.env.oauthApiNamespace;
            axios_1.default.post(`http://${host}${port}/${namespace}/TokenValidation`, null, {
                headers: {
                    Authorization: auth,
                },
            }).then((response) => {
                if (response.data.error !== undefined) {
                    phLogger_1.default.error("auth error");
                    res.status(500).send(response.data);
                    return;
                }
                else {
                    next();
                }
            }).catch((error) => {
                phLogger_1.default.error("auth error");
                res.status(500).send(error);
                return;
            });
        });
        this.router.post("/callR", (req, res, next) => {
            // 临时R计算
            let configFile = "";
            if (req.body.type === "tm") {
                configFile = "pharbers-resources/TM_Submit_New.json";
            }
            else if (req.body.type === "ucb") {
                configFile = "pharbers-resources/UCB_Submit_New.json";
            }
            else {
                phLogger_1.default.warn("unkonwn calc type!");
                configFile = "";
            }
            const httpCallRUrl = this.conf.env.httpCallRUrl;
            const uuid = this.uuidv4();
            axios_1.default.post(httpCallRUrl, {
                jobId: uuid,
                processConfig: configFile,
                processConfigType: "json",
                processLocation: "oss",
                replace: {
                    jobId: uuid,
                    periodId: req.body.periodId,
                    phase: req.body.phase,
                    projectId: req.body.projectId,
                    proposalId: req.body.proposalId,
                },
            }).then((response) => {
                phLogger_1.default.info("R ok");
                res.status(200).send(response.data);
                return;
            }).catch((error) => {
                phLogger_1.default.error("R error");
                phLogger_1.default.error(error);
                res.status(500).send(error);
                return;
            });
        });
        // Add routes for export data to excel
        const exportRoute = "/export/:projectId/phase/:phase";
        const exportInputRoute = "/exportInput/:projectId/phase/:phase";
        this.router.get(exportRoute, (req, res) => __awaiter(this, void 0, void 0, function* () {
            res.json({
                jobId: yield this.exportHandler.export2OssWithProject(req.params.projectId, req.params.phase, true)
            });
        }));
        this.router.get(exportInputRoute, (req, res) => __awaiter(this, void 0, void 0, function* () {
            res.json({
                // tslint:disable-next-line: max-line-length
                jobId: yield this.exportHandler.export2OssWithProject(req.params.projectId, req.params.phase, false)
            });
        }));
        // Add kafka producer
        // const kfkTestRoute = "/kfk"
        // this.router.get(kfkTestRoute, async (req, res) => {
        //     const value = { "records": [ { "value" : { "test" : "alfred test" } } ] }
        //     this.kafka.pushMessage(value)
        //     res.json( {
        //         jobId: "heiheihei"
        //     } )
        // } )
        this.app.use("/", this.router);
    }
    loadConfiguration() {
        try {
            const path = process.env.PH_TS_SERVER_HOME + "/conf";
            const jsonConvert = new json2typescript_1.JsonConvert();
            const doc = yaml.safeLoad(fs.readFileSync(path + "/server.yml", "utf8"));
            // jsonConvert.operationMode = OperationMode.LOGGING // print some debug data
            jsonConvert.ignorePrimitiveChecks = false; // don't allow assigning number to string etc.
            jsonConvert.valueCheckingMode = json2typescript_1.ValueCheckingMode.DISALLOW_NULL; // never allow null
            this.conf = jsonConvert.deserializeObject(doc, serverConf_1.ServerConf);
            this.exportHandler = new ExportProject_1.default(this.conf.oss);
            this.kafka = new KafkaDelegate_1.default(this.conf.kfk);
        }
        catch (e) {
            phLogger_1.default.fatal(e);
        }
    }
    generateModels() {
        const prefix = "/dist/src/models/";
        const path = process.env.PH_TS_SERVER_HOME + prefix;
        const suffix = ".js";
        const result = {};
        this.conf.models.forEach((ele) => {
            const filename = path + ele.file + suffix;
            const one = require(filename).default;
            result[ele.file] = new one().getModel();
        });
        return result;
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
            mongoose.connect(prefix + "://" + username + ":" + pwd + "@" + host + ":" + port + "/" + coll + "?authSource=" + authSource, { useNewUrlParser: true }, (err) => {
                if (err != null) {
                    phLogger_1.default.error(err);
                }
            });
        }
        else {
            phLogger_1.default.info(`connect mongodb without auth`);
            mongoose.connect(prefix + "://" + host + ":" + port + "/" + coll, { useNewUrlParser: true }, (err) => {
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
    generateRoutes(registry) {
        const opts = {
            filterParser: urlEncodeFilterParser_1.urlEncodeFilterParser
        };
        const Front = new json_api_1.default.httpStrategies.Express(new json_api_1.default.controllers.API(registry, opts), new json_api_1.default.controllers.Documentation(registry, { name: "Pharbers API" }));
        // PhLogger.startConnectLog(this.app)
        this.app.get("/", Front.docsRequest);
        const perfix = "/:type";
        const ms = this.conf.models.map((x) => x.reg).join("|");
        const suffix = "/:id";
        const all = perfix + "(" + ms + ")";
        const one = all + suffix;
        const relation = one + "/relationships/:relationship";
        // Add routes for basic list, read, create, update, delete operations
        this.app.get(all, Front.apiRequest);
        this.app.get(one, Front.apiRequest);
        this.app.post(all, Front.apiRequest);
        this.app.patch(one, Front.apiRequest);
        this.app.delete(one, Front.apiRequest);
        // Add routes for adding to, removing from, or updating resource relationships
        this.app.post(relation, Front.apiRequest);
        this.app.patch(relation, Front.apiRequest);
        this.app.delete(relation, Front.apiRequest);
    }
    listen2Port(port) {
        // start the Express server
        this.app.listen(port, () => {
            phLogger_1.default.info(`server started at http://localhost:${port}`);
        });
    }
}
exports.default = AppDelegate;
//# sourceMappingURL=appDelegate.js.map