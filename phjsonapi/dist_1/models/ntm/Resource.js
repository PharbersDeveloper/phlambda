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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var Resource_1;
"use strict";
const json2typescript_1 = require("json2typescript");
const typegoose_1 = require("typegoose");
const Image_1 = __importDefault(require("./Image"));
let Resource = Resource_1 = class Resource extends typegoose_1.Typegoose {
    constructor() {
        super(...arguments);
        this.name = "";
        this.gender = 0;
        this.age = 0;
        this.education = "";
        this.professional = "";
        this.advantage = "";
        this.evaluation = "";
        this.experience = 0;
        this.totalTime = 100;
        this.entryTime = 1;
        this.avatarPath = "";
    }
    getModel() {
        return this.getModelForClass(Resource_1);
    }
};
__decorate([
    json2typescript_1.JsonProperty("name", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Resource.prototype, "name", void 0);
__decorate([
    json2typescript_1.JsonProperty("gender", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Resource.prototype, "gender", void 0);
__decorate([
    json2typescript_1.JsonProperty("age", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Resource.prototype, "age", void 0);
__decorate([
    json2typescript_1.JsonProperty("education", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Resource.prototype, "education", void 0);
__decorate([
    json2typescript_1.JsonProperty("professional", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Resource.prototype, "professional", void 0);
__decorate([
    json2typescript_1.JsonProperty("advantage", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Resource.prototype, "advantage", void 0);
__decorate([
    json2typescript_1.JsonProperty("evaluation", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Resource.prototype, "evaluation", void 0);
__decorate([
    json2typescript_1.JsonProperty("experience", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Resource.prototype, "experience", void 0);
__decorate([
    json2typescript_1.JsonProperty("totalTime", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Resource.prototype, "totalTime", void 0);
__decorate([
    json2typescript_1.JsonProperty("entryTime", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Resource.prototype, "entryTime", void 0);
__decorate([
    typegoose_1.prop({ ref: Image_1.default, required: true }),
    __metadata("design:type", Object)
], Resource.prototype, "avatar", void 0);
__decorate([
    json2typescript_1.JsonProperty("avatar", String),
    __metadata("design:type", String)
], Resource.prototype, "avatarPath", void 0);
Resource = Resource_1 = __decorate([
    json2typescript_1.JsonObject("Resource")
], Resource);
exports.default = Resource;
//# sourceMappingURL=Resource.js.map