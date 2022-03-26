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
var Hospital_1;
"use strict";
const json2typescript_1 = require("json2typescript");
const typegoose_1 = require("typegoose");
const Image_1 = __importDefault(require("./Image"));
const Policy_1 = __importDefault(require("./Policy"));
const Region_1 = __importDefault(require("./Region"));
let Hospital = Hospital_1 = class Hospital extends typegoose_1.Typegoose {
    constructor() {
        super(...arguments);
        this.name = "";
        this.describe = "";
        this.regtime = "";
        this.position = "";
        this.code = "";
        this.avatarPath = "";
        this.category = "";
        this.level = "";
        this.docterNumber = 0;
        this.bedNumber = 0;
        this.income = 0;
        this.spaceBelongs = "";
        this.abilityToPay = "";
        this.selfPayPercentage = 0.0;
        this.patientNum = 0.0;
        this.patientNumA = 0.0;
        this.patientNumB = 0.0;
    }
    getModel() {
        return this.getModelForClass(Hospital_1);
    }
};
__decorate([
    json2typescript_1.JsonProperty("name", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Hospital.prototype, "name", void 0);
__decorate([
    json2typescript_1.JsonProperty("describe", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Hospital.prototype, "describe", void 0);
__decorate([
    json2typescript_1.JsonProperty("regtime", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Hospital.prototype, "regtime", void 0);
__decorate([
    json2typescript_1.JsonProperty("position", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Hospital.prototype, "position", void 0);
__decorate([
    json2typescript_1.JsonProperty("code", String),
    typegoose_1.prop({}),
    __metadata("design:type", String)
], Hospital.prototype, "code", void 0);
__decorate([
    typegoose_1.prop({ ref: Image_1.default, required: true }),
    __metadata("design:type", Object)
], Hospital.prototype, "avatar", void 0);
__decorate([
    json2typescript_1.JsonProperty("avatar", String),
    __metadata("design:type", String)
], Hospital.prototype, "avatarPath", void 0);
__decorate([
    json2typescript_1.JsonProperty("category", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Hospital.prototype, "category", void 0);
__decorate([
    json2typescript_1.JsonProperty("level", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Hospital.prototype, "level", void 0);
__decorate([
    json2typescript_1.JsonProperty("doctorNumber", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Hospital.prototype, "docterNumber", void 0);
__decorate([
    json2typescript_1.JsonProperty("bedNumber", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Hospital.prototype, "bedNumber", void 0);
__decorate([
    json2typescript_1.JsonProperty("income", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Hospital.prototype, "income", void 0);
__decorate([
    json2typescript_1.JsonProperty("spaceBelongs", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Hospital.prototype, "spaceBelongs", void 0);
__decorate([
    json2typescript_1.JsonProperty("abilityToPay", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Hospital.prototype, "abilityToPay", void 0);
__decorate([
    json2typescript_1.JsonProperty("selfPayPercentage", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Hospital.prototype, "selfPayPercentage", void 0);
__decorate([
    json2typescript_1.JsonProperty("patientNum", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Hospital.prototype, "patientNum", void 0);
__decorate([
    json2typescript_1.JsonProperty("patientNumA", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Hospital.prototype, "patientNumA", void 0);
__decorate([
    json2typescript_1.JsonProperty("patientNumB", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Hospital.prototype, "patientNumB", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: Policy_1.default, required: true }),
    __metadata("design:type", Array)
], Hospital.prototype, "policies", void 0);
__decorate([
    typegoose_1.prop({ ref: Region_1.default, required: true }),
    __metadata("design:type", Object)
], Hospital.prototype, "region", void 0);
Hospital = Hospital_1 = __decorate([
    json2typescript_1.JsonObject("Hospital")
], Hospital);
exports.default = Hospital;
//# sourceMappingURL=Hospital.js.map