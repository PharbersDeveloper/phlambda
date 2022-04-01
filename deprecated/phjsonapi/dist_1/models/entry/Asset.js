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
const DataSet_1 = __importDefault(require("./DataSet"));
const DbSource_1 = __importDefault(require("./DbSource"));
const File_1 = __importDefault(require("./File"));
const Mart_1 = __importDefault(require("./Mart"));
class Asset extends typegoose_1.Typegoose {
    getModel() {
        return this.getModelForClass(Asset);
    }
}
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], Asset.prototype, "name", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: false }),
    __metadata("design:type", String)
], Asset.prototype, "description", void 0);
__decorate([
    typegoose_1.prop({ default: "auto robot", required: true }),
    __metadata("design:type", String)
], Asset.prototype, "owner", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], Asset.prototype, "accessibility", void 0);
__decorate([
    typegoose_1.prop({ default: "0.0.0", required: true }),
    __metadata("design:type", String)
], Asset.prototype, "version", void 0);
__decorate([
    typegoose_1.prop({ default: true, required: true }),
    __metadata("design:type", Boolean)
], Asset.prototype, "isNewVersion", void 0);
__decorate([
    typegoose_1.prop({ default: "file", required: true }),
    __metadata("design:type", String)
], Asset.prototype, "dataType", void 0);
__decorate([
    typegoose_1.prop({ ref: File_1.default, required: false }),
    __metadata("design:type", Object)
], Asset.prototype, "file", void 0);
__decorate([
    typegoose_1.prop({ ref: DbSource_1.default, required: false }),
    __metadata("design:type", Object)
], Asset.prototype, "dbs", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: DataSet_1.default, required: false }),
    __metadata("design:type", Array)
], Asset.prototype, "dfs", void 0);
__decorate([
    typegoose_1.prop({ ref: Mart_1.default, required: false }),
    __metadata("design:type", Object)
], Asset.prototype, "mart", void 0);
__decorate([
    typegoose_1.arrayProp({ items: String, default: [], required: false }),
    __metadata("design:type", Array)
], Asset.prototype, "martTags", void 0);
__decorate([
    typegoose_1.arrayProp({ items: String, default: [], required: true }),
    __metadata("design:type", Array)
], Asset.prototype, "providers", void 0);
__decorate([
    typegoose_1.arrayProp({ items: String, default: [], required: true }),
    __metadata("design:type", Array)
], Asset.prototype, "markets", void 0);
__decorate([
    typegoose_1.arrayProp({ items: String, default: [], required: true }),
    __metadata("design:type", Array)
], Asset.prototype, "molecules", void 0);
__decorate([
    typegoose_1.arrayProp({ items: String, default: [], required: true }),
    __metadata("design:type", Array)
], Asset.prototype, "dataCover", void 0);
__decorate([
    typegoose_1.arrayProp({ items: String, default: [], required: true }),
    __metadata("design:type", Array)
], Asset.prototype, "geoCover", void 0);
__decorate([
    typegoose_1.arrayProp({ items: String, default: [], required: true }),
    __metadata("design:type", Array)
], Asset.prototype, "labels", void 0);
__decorate([
    typegoose_1.prop({ default: 0, required: false }),
    __metadata("design:type", Number)
], Asset.prototype, "createTime", void 0);
exports.default = Asset;
//# sourceMappingURL=Asset.js.map