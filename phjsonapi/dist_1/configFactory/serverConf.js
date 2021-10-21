"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const json2typescript_1 = require("json2typescript");
const envConf_1 = require("./envConf");
const kfkConf_1 = require("./kfkConf");
const modelConf_1 = require("./modelConf");
const mongoConf_1 = require("./mongoConf");
const ossConf_1 = require("./ossConf");
let ServerConf = class ServerConf {
    constructor() {
        this.project = undefined;
        this.models = undefined;
        this.mongo = undefined;
        this.env = undefined;
        this.oss = undefined;
        this.kfk = undefined;
    }
};
__decorate([
    json2typescript_1.JsonProperty("project", String),
    __metadata("design:type", String)
], ServerConf.prototype, "project", void 0);
__decorate([
    json2typescript_1.JsonProperty("models", [modelConf_1.ModelConf]),
    __metadata("design:type", Array)
], ServerConf.prototype, "models", void 0);
__decorate([
    json2typescript_1.JsonProperty("mongo", mongoConf_1.MongoConf),
    __metadata("design:type", mongoConf_1.MongoConf)
], ServerConf.prototype, "mongo", void 0);
__decorate([
    json2typescript_1.JsonProperty("env", envConf_1.EnvConf),
    __metadata("design:type", envConf_1.EnvConf)
], ServerConf.prototype, "env", void 0);
__decorate([
    json2typescript_1.JsonProperty("oss", ossConf_1.OssConf),
    __metadata("design:type", ossConf_1.OssConf)
], ServerConf.prototype, "oss", void 0);
__decorate([
    json2typescript_1.JsonProperty("kfk", kfkConf_1.KfkConf),
    __metadata("design:type", kfkConf_1.KfkConf)
], ServerConf.prototype, "kfk", void 0);
ServerConf = __decorate([
    json2typescript_1.JsonObject("ServerConf")
], ServerConf);
exports.ServerConf = ServerConf;
//# sourceMappingURL=serverConf.js.map