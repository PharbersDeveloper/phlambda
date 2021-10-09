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
const FileVersion_1 = __importDefault(require("./FileVersion"));
class FileDetail extends typegoose_1.Typegoose {
    getModel() {
        return this.getModelForClass(FileDetail);
    }
}
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], FileDetail.prototype, "name", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], FileDetail.prototype, "extension", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: true }),
    __metadata("design:type", Number)
], FileDetail.prototype, "created", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], FileDetail.prototype, "kind", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], FileDetail.prototype, "ownerID", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], FileDetail.prototype, "ownerName", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], FileDetail.prototype, "groupID", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: false }),
    __metadata("design:type", String)
], FileDetail.prototype, "traceID", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], FileDetail.prototype, "mod", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: FileVersion_1.default, required: true }),
    __metadata("design:type", Array)
], FileDetail.prototype, "versions", void 0);
__decorate([
    typegoose_1.arrayProp({ items: String, required: true }),
    __metadata("design:type", Array)
], FileDetail.prototype, "jobIds", void 0);
exports.default = FileDetail;
//# sourceMappingURL=FileDetail.js.map