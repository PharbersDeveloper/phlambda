'use strict';
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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.InitServerConf = void 0;
const fs = __importStar(require("fs"));
const yaml = __importStar(require("js-yaml"));
const json2typescript_1 = require("json2typescript");
const ServerConf_1 = require("../configFactory/ServerConf");
const PhLogger_1 = __importDefault(require("../logger/PhLogger"));
class InitServerConf {
    static init() {
        let path = `${process.cwd()}/config/server.yml`;
        if (!fs.existsSync(path)) {
            path = `${__filename.substring(0, __filename.indexOf('lib'))}config/server.yml`;
        }
        PhLogger_1.default.debug('加载配置文件地址', path);
        const jsonConvert = new json2typescript_1.JsonConvert();
        const doc = yaml.safeLoad(fs.readFileSync(path, 'utf8'));
        jsonConvert.ignorePrimitiveChecks = false;
        jsonConvert.valueCheckingMode = json2typescript_1.ValueCheckingMode.DISALLOW_NULL;
        InitServerConf.conf = jsonConvert.deserializeObject(doc, ServerConf_1.ServerConf);
    }
    static get getConf() {
        if (InitServerConf.conf == null) {
            this.init();
        }
        return InitServerConf.conf;
    }
}
exports.InitServerConf = InitServerConf;
