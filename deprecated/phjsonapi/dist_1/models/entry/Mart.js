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
class Mart extends typegoose_1.Typegoose {
    getModel() {
        return this.getModelForClass(Mart);
    }
}
__decorate([
    typegoose_1.arrayProp({ itemsRef: DataSet_1.default, required: false }),
    __metadata("design:type", Array)
], Mart.prototype, "dfs", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], Mart.prototype, "name", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], Mart.prototype, "url", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], Mart.prototype, "dataType", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: false }),
    __metadata("design:type", String)
], Mart.prototype, "description", void 0);
exports.default = Mart;
//# sourceMappingURL=Mart.js.map