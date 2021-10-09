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
class File extends typegoose_1.Typegoose {
    getModel() {
        return this.getModelForClass(File);
    }
}
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], File.prototype, "fileName", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], File.prototype, "extension", void 0);
__decorate([
    typegoose_1.prop({ default: Number, required: true }),
    __metadata("design:type", Number)
], File.prototype, "size", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], File.prototype, "url", void 0);
exports.default = File;
//# sourceMappingURL=File.js.map