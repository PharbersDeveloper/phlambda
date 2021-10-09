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
exports.ServerConf = void 0;
const json2typescript_1 = require("json2typescript");
const mongoConf_1 = require("./mongoConf");
const postgresConf_1 = require("./postgresConf");
let ServerConf = class ServerConf {
    constructor() {
        this.project = undefined;
        this.mongo = undefined;
        this.postgres = undefined;
    }
};
__decorate([
    json2typescript_1.JsonProperty("project", String),
    __metadata("design:type", String)
], ServerConf.prototype, "project", void 0);
__decorate([
    json2typescript_1.JsonProperty("mongo", mongoConf_1.MongoConf),
    __metadata("design:type", mongoConf_1.MongoConf)
], ServerConf.prototype, "mongo", void 0);
__decorate([
    json2typescript_1.JsonProperty("postgres", postgresConf_1.PostgresConf),
    __metadata("design:type", postgresConf_1.PostgresConf)
], ServerConf.prototype, "postgres", void 0);
ServerConf = __decorate([
    json2typescript_1.JsonObject("ServerConf")
], ServerConf);
exports.ServerConf = ServerConf;
//# sourceMappingURL=serverConf.js.map