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
exports.MongoConf = void 0;
const json2typescript_1 = require("json2typescript");
let MongoConf = class MongoConf {
    constructor() {
        this.algorithm = undefined;
        this.host = undefined;
        this.port = undefined;
        this.username = undefined;
        this.pwd = undefined;
        this.coll = undefined;
        this.authSource = undefined;
        this.auth = false;
    }
};
__decorate([
    json2typescript_1.JsonProperty("algorithm", String),
    __metadata("design:type", String)
], MongoConf.prototype, "algorithm", void 0);
__decorate([
    json2typescript_1.JsonProperty("host", String),
    __metadata("design:type", String)
], MongoConf.prototype, "host", void 0);
__decorate([
    json2typescript_1.JsonProperty("port", Number),
    __metadata("design:type", Number)
], MongoConf.prototype, "port", void 0);
__decorate([
    json2typescript_1.JsonProperty("username", String),
    __metadata("design:type", String)
], MongoConf.prototype, "username", void 0);
__decorate([
    json2typescript_1.JsonProperty("pwd", String),
    __metadata("design:type", String)
], MongoConf.prototype, "pwd", void 0);
__decorate([
    json2typescript_1.JsonProperty("coll", String),
    __metadata("design:type", String)
], MongoConf.prototype, "coll", void 0);
__decorate([
    json2typescript_1.JsonProperty("authSource", String),
    __metadata("design:type", String)
], MongoConf.prototype, "authSource", void 0);
__decorate([
    json2typescript_1.JsonProperty("auth", Boolean),
    __metadata("design:type", Boolean)
], MongoConf.prototype, "auth", void 0);
MongoConf = __decorate([
    json2typescript_1.JsonObject("MongoConf")
], MongoConf);
exports.MongoConf = MongoConf;
//# sourceMappingURL=mongoConf.js.map