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
let EnvConf = class EnvConf {
    constructor() {
        this.oauthHost = undefined;
        this.oauthPort = undefined;
        this.oauthApiNamespace = undefined;
        this.kafkaBrokerList = undefined;
        this.kafkaTopic = undefined;
        this.kafkaSecretsDir = undefined;
        this.kafkaPassword = undefined;
        this.schemaRegisterHost = undefined;
        this.httpCallUrl = undefined;
        this.httpCallRUrl = undefined;
    }
};
__decorate([
    json2typescript_1.JsonProperty("oauthHost", String),
    __metadata("design:type", String)
], EnvConf.prototype, "oauthHost", void 0);
__decorate([
    json2typescript_1.JsonProperty("oauthPort", String),
    __metadata("design:type", String)
], EnvConf.prototype, "oauthPort", void 0);
__decorate([
    json2typescript_1.JsonProperty("oauthApiNamespace", String),
    __metadata("design:type", String)
], EnvConf.prototype, "oauthApiNamespace", void 0);
__decorate([
    json2typescript_1.JsonProperty("kafkaBrokerList", String),
    __metadata("design:type", String)
], EnvConf.prototype, "kafkaBrokerList", void 0);
__decorate([
    json2typescript_1.JsonProperty("kafkaTopic", String),
    __metadata("design:type", String)
], EnvConf.prototype, "kafkaTopic", void 0);
__decorate([
    json2typescript_1.JsonProperty("kafkaSecretsDir", String),
    __metadata("design:type", String)
], EnvConf.prototype, "kafkaSecretsDir", void 0);
__decorate([
    json2typescript_1.JsonProperty("kafkaPassword", String),
    __metadata("design:type", String)
], EnvConf.prototype, "kafkaPassword", void 0);
__decorate([
    json2typescript_1.JsonProperty("schemaRegisterHost", String),
    __metadata("design:type", String)
], EnvConf.prototype, "schemaRegisterHost", void 0);
__decorate([
    json2typescript_1.JsonProperty("httpCallUrl", String),
    __metadata("design:type", String)
], EnvConf.prototype, "httpCallUrl", void 0);
__decorate([
    json2typescript_1.JsonProperty("httpCallRUrl", String),
    __metadata("design:type", String)
], EnvConf.prototype, "httpCallRUrl", void 0);
EnvConf = __decorate([
    json2typescript_1.JsonObject("EnvConf")
], EnvConf);
exports.EnvConf = EnvConf;
//# sourceMappingURL=envConf.js.map