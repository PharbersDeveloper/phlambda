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
var Requirement_1;
"use strict";
const json2typescript_1 = require("json2typescript");
const typegoose_1 = require("typegoose");
let Requirement = Requirement_1 = class Requirement extends typegoose_1.Typegoose {
    constructor() {
        super(...arguments);
        this.totalQuotas = 0;
        this.meetingPlaces = 0;
        this.visitingHours = 0;
        this.teamExperience = "";
        this.managerKpi = 0;
        this.mangementHours = 0;
        this.totalBudget = 0;
    }
    getModel() {
        return this.getModelForClass(Requirement_1);
    }
};
__decorate([
    json2typescript_1.JsonProperty("totalQuotas", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Requirement.prototype, "totalQuotas", void 0);
__decorate([
    json2typescript_1.JsonProperty("meetingPlaces", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Requirement.prototype, "meetingPlaces", void 0);
__decorate([
    json2typescript_1.JsonProperty("visitingHours", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Requirement.prototype, "visitingHours", void 0);
__decorate([
    json2typescript_1.JsonProperty("teamExperience", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Requirement.prototype, "teamExperience", void 0);
__decorate([
    json2typescript_1.JsonProperty("teamDescription", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Requirement.prototype, "teamDescription", void 0);
__decorate([
    json2typescript_1.JsonProperty("managerKpi", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Requirement.prototype, "managerKpi", void 0);
__decorate([
    json2typescript_1.JsonProperty("managementHours", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Requirement.prototype, "mangementHours", void 0);
__decorate([
    json2typescript_1.JsonProperty("totalBudget", Number),
    typegoose_1.prop({ required: false, default: 0 }),
    __metadata("design:type", Number)
], Requirement.prototype, "totalBudget", void 0);
Requirement = Requirement_1 = __decorate([
    json2typescript_1.JsonObject("Requirement")
], Requirement);
exports.default = Requirement;
//# sourceMappingURL=Requirement.js.map