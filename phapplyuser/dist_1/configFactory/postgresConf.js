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
exports.PostgresConf = void 0;
const json2typescript_1 = require("json2typescript");
let PostgresConf = class PostgresConf {
    constructor() {
        this.algorithm = undefined;
        this.host = undefined;
        this.port = undefined;
        this.username = undefined;
        this.pwd = undefined;
        this.dbName = undefined;
    }
};
__decorate([
    json2typescript_1.JsonProperty("algorithm", String),
    __metadata("design:type", String)
], PostgresConf.prototype, "algorithm", void 0);
__decorate([
    json2typescript_1.JsonProperty("host", String),
    __metadata("design:type", String)
], PostgresConf.prototype, "host", void 0);
__decorate([
    json2typescript_1.JsonProperty("port", Number),
    __metadata("design:type", Number)
], PostgresConf.prototype, "port", void 0);
__decorate([
    json2typescript_1.JsonProperty("username", String),
    __metadata("design:type", String)
], PostgresConf.prototype, "username", void 0);
__decorate([
    json2typescript_1.JsonProperty("pwd", String),
    __metadata("design:type", String)
], PostgresConf.prototype, "pwd", void 0);
__decorate([
    json2typescript_1.JsonProperty("dbName", String),
    __metadata("design:type", String)
], PostgresConf.prototype, "dbName", void 0);
PostgresConf = __decorate([
    json2typescript_1.JsonObject("ServerConf")
], PostgresConf);
exports.PostgresConf = PostgresConf;
//# sourceMappingURL=postgresConf.js.map