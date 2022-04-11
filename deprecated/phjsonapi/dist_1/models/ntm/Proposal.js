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
var Proposal_1;
"use strict";
const json2typescript_1 = require("json2typescript");
const typegoose_1 = require("typegoose");
const Evaluation_1 = __importDefault(require("./Evaluation"));
const Hospital_1 = __importDefault(require("./Hospital"));
const Product_1 = __importDefault(require("./Product"));
const Requirement_1 = __importDefault(require("./Requirement"));
const Resource_1 = __importDefault(require("./Resource"));
const Validation_1 = __importDefault(require("./Validation"));
// import mongoose = require("mongoose")
let Proposal = Proposal_1 = class Proposal extends typegoose_1.Typegoose {
    // import mongoose = require("mongoose")
    constructor() {
        super(...arguments);
        this.name = "";
        this.describe = "";
        this.totalPhase = 1;
        this.case = "";
        this.periodStep = "";
        this.periodBase = 0;
    }
    getModel() {
        return this.getModelForClass(Proposal_1);
    }
};
__decorate([
    json2typescript_1.JsonProperty("name", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Proposal.prototype, "name", void 0);
__decorate([
    json2typescript_1.JsonProperty("describe", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Proposal.prototype, "describe", void 0);
__decorate([
    json2typescript_1.JsonProperty("totalPhase", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Proposal.prototype, "totalPhase", void 0);
__decorate([
    json2typescript_1.JsonProperty("case", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Proposal.prototype, "case", void 0);
__decorate([
    json2typescript_1.JsonProperty("periodStep", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Proposal.prototype, "periodStep", void 0);
__decorate([
    json2typescript_1.JsonProperty("periodBase", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Proposal.prototype, "periodBase", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: Product_1.default, required: false, default: [] }),
    __metadata("design:type", Array)
], Proposal.prototype, "products", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: Hospital_1.default, required: false, default: [] }),
    __metadata("design:type", Array)
], Proposal.prototype, "targets", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: Resource_1.default, required: false, default: [] }),
    __metadata("design:type", Array)
], Proposal.prototype, "resources", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: Evaluation_1.default, required: false, default: [] }),
    __metadata("design:type", Array)
], Proposal.prototype, "evaluations", void 0);
__decorate([
    typegoose_1.prop({ ref: Requirement_1.default, required: false, default: [] }),
    __metadata("design:type", Object)
], Proposal.prototype, "quota", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: Validation_1.default, required: false, default: [] }),
    __metadata("design:type", Array)
], Proposal.prototype, "validations", void 0);
Proposal = Proposal_1 = __decorate([
    json2typescript_1.JsonObject("Proposal")
], Proposal);
exports.default = Proposal;
//# sourceMappingURL=Proposal.js.map