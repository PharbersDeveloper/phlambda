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
const Answer_1 = __importDefault(require("./Answer"));
const Report_1 = __importDefault(require("./Report"));
class Period extends typegoose_1.Typegoose {
    constructor() {
        super(...arguments);
        this.phase = 0;
    }
    // 反向绑定
    // @arrayProp( { itemsRef: Preset, default: []} )
    // public presets?: Array<Ref<Preset>>
    getModel() {
        return this.getModelForClass(Period);
    }
}
__decorate([
    typegoose_1.prop({ required: true, default: 0 }),
    __metadata("design:type", Number)
], Period.prototype, "phase", void 0);
__decorate([
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Period.prototype, "name", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: Answer_1.default, required: true }),
    __metadata("design:type", Array)
], Period.prototype, "answers", void 0);
__decorate([
    typegoose_1.arrayProp({ itemsRef: Report_1.default, required: true }),
    __metadata("design:type", Array)
], Period.prototype, "reports", void 0);
exports.default = Period;
//# sourceMappingURL=Period.js.map