'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.DBConf = void 0;
const json2typescript_1 = require("json2typescript");
let DBConf = class DBConf {
    constructor() {
        this.algorithm = undefined;
        this.host = undefined;
        this.port = undefined;
        this.dao = undefined;
        this.username = undefined;
        this.pwd = undefined;
    }
};
__decorate([
    json2typescript_1.JsonProperty('algorithm', String)
], DBConf.prototype, "algorithm", void 0);
__decorate([
    json2typescript_1.JsonProperty('host', String)
], DBConf.prototype, "host", void 0);
__decorate([
    json2typescript_1.JsonProperty('port', Number)
], DBConf.prototype, "port", void 0);
__decorate([
    json2typescript_1.JsonProperty('dao', String, true)
], DBConf.prototype, "dao", void 0);
__decorate([
    json2typescript_1.JsonProperty('username', String, true)
], DBConf.prototype, "username", void 0);
__decorate([
    json2typescript_1.JsonProperty('pwd', String, true)
], DBConf.prototype, "pwd", void 0);
DBConf = __decorate([
    json2typescript_1.JsonObject('DBConf')
], DBConf);
exports.DBConf = DBConf;
