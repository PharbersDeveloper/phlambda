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
const Datasource_1 = __importDefault(require("./Datasource"));
class Component extends typegoose_1.Typegoose {
    getModel() {
        return this.getModelForClass(Component);
    }
}
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], Component.prototype, "name", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], Component.prototype, "description", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], Component.prototype, "owner", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: false }),
    __metadata("design:type", String)
], Component.prototype, "cat", void 0);
__decorate([
    typegoose_1.prop({ ref: Datasource_1.default, required: false }),
    __metadata("design:type", Object)
], Component.prototype, "dataSource", void 0);
__decorate([
    typegoose_1.prop({ default: "", required: true }),
    __metadata("design:type", String)
], Component.prototype, "hbs", void 0);
exports.default = Component;
//# sourceMappingURL=Component.js.map