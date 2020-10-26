'use strict';
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
const StoreEnum_1 = require("../../common/StoreEnum");
const DBFactory_1 = __importDefault(require("../../factory/DBFactory"));
class RedisStore {
    constructor() {
        this.store = DBFactory_1.default.getInstance.getStore(StoreEnum_1.StoreEnum.Redis);
    }
    static get getInstance() {
        if (RedisStore.instance == null) {
            RedisStore.instance = new RedisStore();
        }
        return RedisStore.instance;
    }
    setExpire(key, value, expire) {
        return __awaiter(this, void 0, void 0, function* () {
            if (this.store === undefined) {
                throw new Error('Redis Store未实例化，请检查配置');
            }
            yield this.store.adapter.redis.set(key, value, 'EX', expire);
        });
    }
    open() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.store.connect();
        });
    }
    close() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.store.disconnect();
        });
    }
}
exports.default = RedisStore;
RedisStore.instance = null;
