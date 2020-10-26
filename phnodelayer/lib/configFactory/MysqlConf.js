'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.MysqlConf = void 0;
const json2typescript_1 = require("json2typescript");
const DBConf_1 = require("./DBConf");
let MysqlConf = class MysqlConf extends DBConf_1.DBConf {
    constructor() {
        super(...arguments);
        this.dbName = undefined;
    }
    getUrl() {
        return `${this.algorithm}://${this.username}:${this.pwd}@${this.host}:${this.port}/${this.dbName}`;
    }
};
__decorate([
    json2typescript_1.JsonProperty('dbName', String)
], MysqlConf.prototype, "dbName", void 0);
MysqlConf = __decorate([
    json2typescript_1.JsonObject('MysqlConf')
], MysqlConf);
exports.MysqlConf = MysqlConf;
