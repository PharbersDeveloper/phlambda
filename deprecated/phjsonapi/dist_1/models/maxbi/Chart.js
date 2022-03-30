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
const Metadata_1 = __importDefault(require("./Metadata"));
class Chart extends typegoose_1.Typegoose {
    getModel() {
        return this.getModelForClass(Chart);
    }
}
__decorate([
    typegoose_1.prop({ ref: Metadata_1.default, default: null, required: true }),
    __metadata("design:type", Object)
], Chart.prototype, "metadata", void 0);
__decorate([
    typegoose_1.prop({ default: null, required: true }),
    __metadata("design:type", Object)
], Chart.prototype, "styleConfigs", void 0);
__decorate([
    typegoose_1.prop({ default: null, required: true }),
    __metadata("design:type", Object)
], Chart.prototype, "dataConfigs", void 0);
__decorate([
    typegoose_1.prop({ default: null, required: true }),
    __metadata("design:type", Object)
], Chart.prototype, "otherConfigs", void 0);
exports.default = Chart;
//# sourceMappingURL=Chart.js.map