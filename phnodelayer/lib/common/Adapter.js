'use strict';
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Adapter = void 0;
const fortune_mongodb_1 = __importDefault(require("fortune-mongodb"));
const fortune_mysql_1 = __importDefault(require("fortune-mysql"));
const fortune_postgres_1 = __importDefault(require("fortune-postgres"));
const fortune_redis_1 = __importDefault(require("fortune-redis"));
const StoreEnum_1 = require("./StoreEnum");
class Adapter {
    constructor() {
        this.adapterMapping = new Map();
        this.adapterMapping.set(StoreEnum_1.StoreEnum.Postgres, fortune_postgres_1.default);
        this.adapterMapping.set(StoreEnum_1.StoreEnum.MongoDB, fortune_mongodb_1.default);
        this.adapterMapping.set(StoreEnum_1.StoreEnum.Mysql, fortune_mysql_1.default);
        this.adapterMapping.set(StoreEnum_1.StoreEnum.Redis, fortune_redis_1.default);
    }
    static get init() {
        if (Adapter.instance === null) {
            Adapter.instance = new Adapter();
        }
        return Adapter.instance;
    }
    getAdapter(name) {
        return this.adapterMapping.get(name);
    }
}
exports.Adapter = Adapter;
Adapter.instance = null;
