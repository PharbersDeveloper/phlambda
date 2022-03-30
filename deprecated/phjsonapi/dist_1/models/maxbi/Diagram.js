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
const typegoose_1 = require("typegoose");
class Diagram extends typegoose_1.Typegoose {
    getModel() {
        return this.getModelForClass(Diagram);
    }
}
__decorate([
    typegoose_1.prop({ default: [], required: true }),
    __metadata("design:type", Array)
], Diagram.prototype, "colorPool", void 0);
__decorate([
    typegoose_1.prop({ default: [], required: true }),
    __metadata("design:type", Array)
], Diagram.prototype, "commonts", void 0);
__decorate([
    typegoose_1.prop({ default: [], required: false }),
    __metadata("design:type", Array)
], Diagram.prototype, "dimension", void 0);
__decorate([
    typegoose_1.prop({ default: [], required: false }),
    __metadata("design:type", Array)
], Diagram.prototype, "dimensions", void 0);
__decorate([
    typegoose_1.prop({ default: [], required: false }),
    __metadata("design:type", Array)
], Diagram.prototype, "measure", void 0);
__decorate([
    typegoose_1.prop({ default: null, required: false }),
    __metadata("design:type", Object)
], Diagram.prototype, "geo", void 0);
__decorate([
    typegoose_1.prop({ default: null, required: false }),
    __metadata("design:type", Object)
], Diagram.prototype, "grid", void 0);
__decorate([
    typegoose_1.prop({ default: null, required: false }),
    __metadata("design:type", Object)
], Diagram.prototype, "pieAxis", void 0);
__decorate([
    typegoose_1.prop({ default: null, required: false }),
    __metadata("design:type", Object)
], Diagram.prototype, "polar", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], Diagram.prototype, "title", void 0);
__decorate([
    typegoose_1.prop({ default: null, required: false }),
    __metadata("design:type", Object)
], Diagram.prototype, "xAxis", void 0);
__decorate([
    typegoose_1.prop({ default: null, required: false }),
    __metadata("design:type", Object)
], Diagram.prototype, "yAxis", void 0);
__decorate([
    typegoose_1.prop({ default: null, required: false }),
    __metadata("design:type", Object)
], Diagram.prototype, "fetch", void 0);
exports.default = Diagram;
//# sourceMappingURL=Diagram.js.map