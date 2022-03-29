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
let OssConf = class OssConf {
    constructor() {
        this.accessKeyId = undefined;
        this.accessKeySecret = undefined;
        this.bucket = undefined;
        this.region = undefined;
    }
};
__decorate([
    json2typescript_1.JsonProperty("accessKeyId", String),
    __metadata("design:type", String)
], OssConf.prototype, "accessKeyId", void 0);
__decorate([
    json2typescript_1.JsonProperty("accessKeySecret", String),
    __metadata("design:type", String)
], OssConf.prototype, "accessKeySecret", void 0);
__decorate([
    json2typescript_1.JsonProperty("bucket", String),
    __metadata("design:type", String)
], OssConf.prototype, "bucket", void 0);
__decorate([
    json2typescript_1.JsonProperty("region", String),
    __metadata("design:type", String)
], OssConf.prototype, "region", void 0);
OssConf = __decorate([
    json2typescript_1.JsonObject("ossConf")
], OssConf);
exports.OssConf = OssConf;
//# sourceMappingURL=ossConf.js.map