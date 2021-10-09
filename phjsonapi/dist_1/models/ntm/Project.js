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
const Final_1 = __importDefault(require("./Final"));
const Period_1 = __importDefault(require("./Period"));
const Proposal_1 = __importDefault(require("./Proposal"));
class Project extends typegoose_1.Typegoose {
    getModel() {
        return this.getModelForClass(Project);
    }
}
__decorate([
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Project.prototype, "accountId", void 0);
__decorate([
    typegoose_1.prop({ ref: Proposal_1.default, required: true }),
    __metadata("design:type", Object)
], Project.prototype, "proposal", void 0);
__decorate([
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Project.prototype, "current", void 0);
__decorate([
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Project.prototype, "pharse", void 0);
__decorate([
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Project.prototype, "status", void 0);
__decorate([
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Project.prototype, "startTime", void 0);
__decorate([
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Project.prototype, "endTime", void 0);
__decorate([
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Project.prototype, "lastUpdate", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: Period_1.default, required: true }),
    __metadata("design:type", Array)
], Project.prototype, "periods", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: Final_1.default, required: true }),
    __metadata("design:type", Array)
], Project.prototype, "finals", void 0);
exports.default = Project;
//# sourceMappingURL=Project.js.map