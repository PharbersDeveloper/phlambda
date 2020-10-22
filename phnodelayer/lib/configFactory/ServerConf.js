'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ServerConf = void 0;
const json2typescript_1 = require("json2typescript");
const MongoConf_1 = require("./MongoConf");
const MysqlConf_1 = require("./MysqlConf");
const PostgresConf_1 = require("./PostgresConf");
const RedisConf_1 = require("./RedisConf");
let ServerConf = class ServerConf {
    constructor() {
        this.project = undefined;
        this.postgres = undefined;
        this.mongo = undefined;
        this.mysql = undefined;
        this.redis = undefined;
    }
};
__decorate([
    json2typescript_1.JsonProperty('project', String)
], ServerConf.prototype, "project", void 0);
__decorate([
    json2typescript_1.JsonProperty('postgres', PostgresConf_1.PostgresConf)
], ServerConf.prototype, "postgres", void 0);
__decorate([
    json2typescript_1.JsonProperty('mongo', MongoConf_1.MongoConf, true)
], ServerConf.prototype, "mongo", void 0);
__decorate([
    json2typescript_1.JsonProperty('mysql', MysqlConf_1.MysqlConf, true)
], ServerConf.prototype, "mysql", void 0);
__decorate([
    json2typescript_1.JsonProperty('redis', RedisConf_1.RedisConf, true)
], ServerConf.prototype, "redis", void 0);
ServerConf = __decorate([
    json2typescript_1.JsonObject('ServerConf')
], ServerConf);
exports.ServerConf = ServerConf;
