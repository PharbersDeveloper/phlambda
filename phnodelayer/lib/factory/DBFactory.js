'use strict';
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const fortune_1 = __importDefault(require("fortune"));
const Adapter_1 = require("../common/Adapter");
const InitServerConf_1 = require("../common/InitServerConf");
class DBFactory {
    constructor() {
        this.typeAnalyzerMapping = new Map();
        this.serverConf = InitServerConf_1.InitServerConf.getConf;
        this.buildStore(this.serverConf);
    }
    static get getInstance() {
        if (DBFactory.instance == null) {
            DBFactory.instance = new DBFactory();
        }
        return DBFactory.instance;
    }
    getStore(name) {
        if (name === undefined || name === null || name.length === 0) {
            if (this.typeAnalyzerMapping.size === 1) {
                return [...this.typeAnalyzerMapping.values()][0];
            }
            else {
                throw new Error(`存在多个Store, 请使用 getStore(参数) 获取对应Store，包含参数：${[...this.typeAnalyzerMapping.keys()]}`);
            }
        }
        return this.typeAnalyzerMapping.get(name);
    }
    buildStore(conf) {
        const keys = Object.getOwnPropertyNames(conf)
            .map((name) => {
            const ins = conf[name];
            if (ins !== undefined && typeof ins !== 'string') {
                return name;
            }
        })
            .filter((item) => item !== undefined);
        let filename = null;
        for (const key of keys) {
            const ad = Adapter_1.Adapter.init.getAdapter(key);
            const url = conf[key].getUrl();
            const path = `${process.cwd()}/dist/models`;
            if (conf[key].dao !== undefined) {
                filename = `${path}/${conf[key].dao}.js`;
            }
            else {
                filename = `${path}/${conf.project}.js`;
            }
            const metaClass = require(filename).default;
            const record = new metaClass();
            const options = Object.assign({ adapter: [ad, { url }] }, record.operations);
            this.typeAnalyzerMapping.set(key, fortune_1.default(record.model, options));
        }
    }
}
exports.default = DBFactory;
DBFactory.instance = null;
