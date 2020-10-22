"use strict";
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
exports.Main = exports.redis = exports.dbFactory = exports.store = exports.logger = void 0;
const PhLogger_1 = __importDefault(require("./logger/PhLogger"));
const appLambdaDelegate_1 = __importDefault(require("./delegate/appLambdaDelegate"));
const StoreEnum_1 = require("./common/StoreEnum");
const DBFactory_1 = __importDefault(require("./factory/DBFactory"));
const RedisStore_1 = __importDefault(require("./strategies/store/RedisStore"));
exports.logger = PhLogger_1.default;
exports.store = StoreEnum_1.StoreEnum;
exports.dbFactory = DBFactory_1.default;
exports.redis = RedisStore_1.default;
exports.Main = (event, db = StoreEnum_1.StoreEnum.Postgres) => __awaiter(void 0, void 0, void 0, function* () {
    exports.logger.debug("进入初始化");
    const del = new appLambdaDelegate_1.default();
    exports.logger.debug("正在创建实例");
    let result = null;
    if (del.isFirstInit) {
        exports.logger.debug("开始连接数据库");
        yield del.prepare(db);
        exports.logger.debug("连接数据库结束");
    }
    if (event !== null && event !== undefined) {
        exports.logger.debug("开始执行请求");
        result = yield del.exec(event);
        exports.logger.debug("执行请求结束");
    }
    yield del.cleanUp();
    exports.logger.debug("关闭数据库");
    return result;
});
