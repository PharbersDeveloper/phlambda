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
const typegoose_1 = require("typegoose");
const AnswerCategory_1 = require("../../enum/AnswerCategory");
const Hospital_1 = __importDefault(require("./Hospital"));
const Product_1 = __importDefault(require("./Product"));
const Resource_1 = __importDefault(require("./Resource"));
class Answer extends typegoose_1.Typegoose {
    getModel() {
        return this.getModelForClass(Answer);
    }
}
__decorate([
    typegoose_1.prop({ enum: AnswerCategory_1.AnswerCategory, required: true }),
    __metadata("design:type", String)
], Answer.prototype, "category", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "salesTarget", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "budget", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "meetingPlaces", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "visitTime", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "productKnowledgeTraining", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "vocationalDevelopment", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "regionTraining", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "performanceTraining", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "salesAbilityTraining", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "assistAccessTime", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "abilityCoach", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "strategAnalysisTime", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "adminWorkTime", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "clientManagementTime", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "kpiAnalysisTime", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], Answer.prototype, "teamMeetingTime", void 0);
__decorate([
    typegoose_1.prop({ ref: Resource_1.default, default: null, required: true }),
    __metadata("design:type", Object)
], Answer.prototype, "resource", void 0);
__decorate([
    typegoose_1.prop({ ref: Product_1.default, default: null, required: true }),
    __metadata("design:type", Object)
], Answer.prototype, "product", void 0);
__decorate([
    typegoose_1.prop({ ref: Hospital_1.default, default: null, required: true }),
    __metadata("design:type", Object)
], Answer.prototype, "target", void 0);
exports.default = Answer;
//# sourceMappingURL=Answer.js.map