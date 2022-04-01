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
var Preset_1;
"use strict";
const json2typescript_1 = require("json2typescript");
const typegoose_1 = require("typegoose");
const Hospital_1 = __importDefault(require("./Hospital"));
const Product_1 = __importDefault(require("./Product"));
const Proposal_1 = __importDefault(require("./Proposal"));
const Resource_1 = __importDefault(require("./Resource"));
let Preset = Preset_1 = class Preset extends typegoose_1.Typegoose {
    constructor() {
        super(...arguments);
        this.phase = 0; //
        this.category = 0; //
        this.lastQuota = 0; // p_quota
        this.lastSales = 0; // p_sales
        this.lastAchievement = 0; // p_sales
        this.potential = 0; // 铁马不变
        this.lastShare = 0; // p_share
        this.currentTMA = 0; // p_territory_management_ability
        this.currentSalesSkills = 0; // p_sales_skills
        this.currentProductKnowledge = 0; // p_product_knowledge
        this.currentBehaviorEfficiency = 0; // p_behavior_efficiency
        this.currentWorkMotivation = 0; // p_work_motivation
        this.currentTargetDoctorNum = 0; // p_target
        this.currentTargetDoctorCoverage = 0.0; // p_target_coverage
        this.currentClsADoctorVT = 0; // p_high_target
        this.currentClsBDoctorVT = 0; // p_middle_target
        this.currentClsCDoctorVT = 0; // p_low_target
        this.currentPatientNum = 0;
        this.currentDurgEntrance = "";
        this.currentPolicy = "";
        this.lastBudget = 0;
        this.initBudget = 0;
    }
    getModel() {
        return this.getModelForClass(Preset_1);
    }
};
__decorate([
    typegoose_1.prop({ ref: Proposal_1.default, required: true, default: null }),
    __metadata("design:type", Object)
], Preset.prototype, "proposal", void 0);
__decorate([
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Preset.prototype, "proposalId", void 0);
__decorate([
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Preset.prototype, "projectId", void 0);
__decorate([
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Preset.prototype, "periodId", void 0);
__decorate([
    typegoose_1.prop({ ref: Product_1.default, required: true, default: null }),
    __metadata("design:type", Object)
], Preset.prototype, "product", void 0);
__decorate([
    typegoose_1.prop({ ref: Hospital_1.default, required: true, default: null }),
    __metadata("design:type", Object)
], Preset.prototype, "hospital", void 0);
__decorate([
    typegoose_1.prop({ ref: Resource_1.default, required: true, default: null }),
    __metadata("design:type", Object)
], Preset.prototype, "resource", void 0);
__decorate([
    json2typescript_1.JsonProperty("phase", Number),
    typegoose_1.prop({ required: true, default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "phase", void 0);
__decorate([
    json2typescript_1.JsonProperty("category", Number),
    typegoose_1.prop({ default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "category", void 0);
__decorate([
    json2typescript_1.JsonProperty("lastQuota", Number),
    typegoose_1.prop({ default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "lastQuota", void 0);
__decorate([
    json2typescript_1.JsonProperty("lastSales", Number),
    typegoose_1.prop({ default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "lastSales", void 0);
__decorate([
    json2typescript_1.JsonProperty("lastAchievement", Number),
    typegoose_1.prop({ default: 0.0 }),
    __metadata("design:type", Number)
], Preset.prototype, "lastAchievement", void 0);
__decorate([
    json2typescript_1.JsonProperty("potential", Number),
    typegoose_1.prop({ default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "potential", void 0);
__decorate([
    json2typescript_1.JsonProperty("lastShare", Number),
    typegoose_1.prop({ default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "lastShare", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentTMA", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "currentTMA", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentSalesSkills", Number),
    typegoose_1.prop({ default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "currentSalesSkills", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentProductKnowledge", Number),
    typegoose_1.prop({ default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "currentProductKnowledge", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentBehaviorEfficiency", Number),
    typegoose_1.prop({ default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "currentBehaviorEfficiency", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentWorkMotivation", Number),
    typegoose_1.prop({ default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "currentWorkMotivation", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentTargetDoctorNum", Number),
    typegoose_1.prop({ default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "currentTargetDoctorNum", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentTargetDoctorCoverage", Number),
    typegoose_1.prop({ default: 0.0 }),
    __metadata("design:type", Number)
], Preset.prototype, "currentTargetDoctorCoverage", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentClsADoctorVT", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "currentClsADoctorVT", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentClsBDoctorVT", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "currentClsBDoctorVT", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentClsADoctorVT", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "currentClsCDoctorVT", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentPatientNum", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "currentPatientNum", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentDurgEntrance", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Preset.prototype, "currentDurgEntrance", void 0);
__decorate([
    json2typescript_1.JsonProperty("currentPolicy", String, false),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Preset.prototype, "currentPolicy", void 0);
__decorate([
    json2typescript_1.JsonProperty("lastBudget", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "lastBudget", void 0);
__decorate([
    json2typescript_1.JsonProperty("initBudget", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Preset.prototype, "initBudget", void 0);
Preset = Preset_1 = __decorate([
    json2typescript_1.JsonObject("Preset")
], Preset);
exports.default = Preset;
//# sourceMappingURL=Preset.js.map