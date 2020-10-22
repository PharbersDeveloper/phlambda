'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.MongoConf = void 0;
const json2typescript_1 = require("json2typescript");
const DBConf_1 = require("./DBConf");
let MongoConf = class MongoConf extends DBConf_1.DBConf {
    constructor() {
        super(...arguments);
        this.coll = undefined;
        this.authSource = undefined;
        this.auth = false;
        this.other = undefined;
    }
    getUrl() {
        return `${this.algorithm}://${this.username}:${this.pwd}@${this.host}/${this.coll}${this.other}`;
    }
};
__decorate([
    json2typescript_1.JsonProperty('coll', String)
], MongoConf.prototype, "coll", void 0);
__decorate([
    json2typescript_1.JsonProperty('authSource', String)
], MongoConf.prototype, "authSource", void 0);
__decorate([
    json2typescript_1.JsonProperty('auth', Boolean)
], MongoConf.prototype, "auth", void 0);
__decorate([
    json2typescript_1.JsonProperty('other', String)
], MongoConf.prototype, "other", void 0);
MongoConf = __decorate([
    json2typescript_1.JsonObject('MongoConf')
], MongoConf);
exports.MongoConf = MongoConf;
