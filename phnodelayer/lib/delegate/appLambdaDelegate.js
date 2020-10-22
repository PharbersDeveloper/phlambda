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
const http_1 = require("http");
const Adapter_1 = require("../common/Adapter");
const InitServerConf_1 = require("../common/InitServerConf");
const DBFactory_1 = __importDefault(require("../factory/DBFactory"));
const AwsRequest_1 = __importDefault(require("../strategies/AwsRequest"));
class AppLambdaDelegate {
    constructor() {
        /**
         * custom 下的包为编译文件 普通 import 会找不到描述文件，暂时解决方案为require导入
         */
        this.fortuneHTTP = require("../../custom/fortune-http");
        this.jsonApiSerializer = require("../../custom/fortune-json-api");
        this.conf = InitServerConf_1.InitServerConf.getConf;
        this.isFirstInit = true;
    }
    prepare(name) {
        return __awaiter(this, void 0, void 0, function* () {
            Adapter_1.Adapter.init;
            this.store = DBFactory_1.default.getInstance.getStore(name);
            yield this.store.connect();
            this.isFirstInit = false;
            this.listener = this.fortuneHTTP(this.store, {
                serializers: [
                    [this.jsonApiSerializer]
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
            if (!event["body"]) {
                event["body"] = "";
            }
            const req = new AwsRequest_1.default(event, this.conf.project);
            const response = new http_1.ServerResponse(req);
            const buffer = Buffer.from(event["body"]);
            // @ts-ignore
            req._readableState.buffer = buffer;
            yield this.listener(req, response, buffer);
            return response;
        });
    }
}
exports.default = AppLambdaDelegate;
