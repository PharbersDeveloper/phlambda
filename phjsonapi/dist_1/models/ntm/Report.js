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
var Report_1;
"use strict";
// import Proposal from "./Proposal"
const json2typescript_1 = require("json2typescript");
const typegoose_1 = require("typegoose");
const ReportCategory_1 = require("../../enum/ReportCategory");
const Hospital_1 = __importDefault(require("./Hospital"));
const Product_1 = __importDefault(require("./Product"));
const Resource_1 = __importDefault(require("./Resource"));
let Report = Report_1 = class Report extends typegoose_1.Typegoose {
    constructor() {
        super(...arguments);
        this.category = ReportCategory_1.ReportCategory.Hospital;
        this.proposalId = "";
        this.projectId = "";
        this.periodId = "";
        this.phase = 0;
        this.region = "";
        // 写到下期
        this.potential = 0;
        // 写到下期
        this.patientNum = 0;
        // 写到下期
        this.drugEntrance = "";
        // 写到下期
        // @JsonProperty("budget", Number)
        // @prop({ required: false, default: 0 })
        // public budget?: number = 0
        this.sales = 0;
        this.salesContri = 0;
        this.salesQuota = 0;
        this.quotaGrowthMOM = 0;
        this.quotaContri = 0;
        this.share = 0;
        this.salesGrowthYOY = 0;
        this.salesGrowthMOM = 0;
        this.achievements = 0;
        this.ytd = 0;
    }
    getModel() {
        return this.getModelForClass(Report_1);
    }
};
__decorate([
    json2typescript_1.JsonProperty("category", String),
    typegoose_1.prop({ enum: ReportCategory_1.ReportCategory, required: true }),
    __metadata("design:type", String)
], Report.prototype, "category", void 0);
__decorate([
    typegoose_1.prop({ default: "" }),
    __metadata("design:type", String)
], Report.prototype, "proposalId", void 0);
__decorate([
    typegoose_1.prop({ default: "" }),
    __metadata("design:type", String)
], Report.prototype, "projectId", void 0);
__decorate([
    typegoose_1.prop({ default: "" }),
    __metadata("design:type", String)
], Report.prototype, "periodId", void 0);
__decorate([
    typegoose_1.prop({ ref: Hospital_1.default, default: null }),
    __metadata("design:type", Object)
], Report.prototype, "hospital", void 0);
__decorate([
    typegoose_1.prop({ ref: Product_1.default, default: null }),
    __metadata("design:type", Object)
], Report.prototype, "product", void 0);
__decorate([
    typegoose_1.prop({ ref: Resource_1.default, default: null }),
    __metadata("design:type", Object)
], Report.prototype, "resource", void 0);
__decorate([
    json2typescript_1.JsonProperty("phase", Number),
    typegoose_1.prop({ required: true, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "phase", void 0);
__decorate([
    json2typescript_1.JsonProperty("region", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Report.prototype, "region", void 0);
__decorate([
    json2typescript_1.JsonProperty("potential", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "potential", void 0);
__decorate([
    json2typescript_1.JsonProperty("patientNum", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "patientNum", void 0);
__decorate([
    json2typescript_1.JsonProperty("drugEntrance", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Report.prototype, "drugEntrance", void 0);
__decorate([
    json2typescript_1.JsonProperty("sales", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "sales", void 0);
__decorate([
    json2typescript_1.JsonProperty("salesContri", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "salesContri", void 0);
__decorate([
    json2typescript_1.JsonProperty("quota", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "salesQuota", void 0);
__decorate([
    json2typescript_1.JsonProperty("quotaGrowthMOM", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "quotaGrowthMOM", void 0);
__decorate([
    json2typescript_1.JsonProperty("quotaContri", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "quotaContri", void 0);
__decorate([
    json2typescript_1.JsonProperty("share", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "share", void 0);
__decorate([
    json2typescript_1.JsonProperty("salesGrowthYOY", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "salesGrowthYOY", void 0);
__decorate([
    json2typescript_1.JsonProperty("salesGrowthMOM", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "salesGrowthMOM", void 0);
__decorate([
    json2typescript_1.JsonProperty("quotaAchievement", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "achievements", void 0);
__decorate([
    json2typescript_1.JsonProperty("ytd", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Report.prototype, "ytd", void 0);
Report = Report_1 = __decorate([
    json2typescript_1.JsonObject("Report")
], Report);
exports.default = Report;
//# sourceMappingURL=Report.js.map