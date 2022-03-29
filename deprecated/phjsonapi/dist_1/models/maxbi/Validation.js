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
var Validation_1;
"use strict";
const json2typescript_1 = require("json2typescript");
const typegoose_1 = require("typegoose");
const ValidationType_1 = require("../../enum/ValidationType");
let Validation = Validation_1 = class Validation extends typegoose_1.Typegoose {
    constructor() {
        super(...arguments);
        this.validationType = ValidationType_1.ValidationType.String;
        this.expression = undefined;
        this.condition = undefined;
        this.error = undefined;
        this.leftValue = undefined;
        this.rightValue = undefined;
    }
    getModel() {
        return this.getModelForClass(Validation_1);
    }
};
__decorate([
    json2typescript_1.JsonProperty("validationType", String),
    typegoose_1.prop({ required: true, default: ValidationType_1.ValidationType.String }),
    __metadata("design:type", Number)
], Validation.prototype, "validationType", void 0);
__decorate([
    json2typescript_1.JsonProperty("expression", String),
    typegoose_1.prop({ required: true, default: "" }),
    __metadata("design:type", String)
], Validation.prototype, "expression", void 0);
__decorate([
    json2typescript_1.JsonProperty("condition", String),
    typegoose_1.prop({ required: true, default: "" }),
    __metadata("design:type", String)
], Validation.prototype, "condition", void 0);
__decorate([
    json2typescript_1.JsonProperty("error", String),
    typegoose_1.prop({ required: true, default: "" }),
    __metadata("design:type", String)
], Validation.prototype, "error", void 0);
__decorate([
    json2typescript_1.JsonProperty("leftValue", String),
    typegoose_1.prop({ required: true, default: "" }),
    __metadata("design:type", String)
], Validation.prototype, "leftValue", void 0);
__decorate([
    json2typescript_1.JsonProperty("rightValue", String),
    typegoose_1.prop({ required: true, default: "" }),
    __metadata("design:type", String)
], Validation.prototype, "rightValue", void 0);
Validation = Validation_1 = __decorate([
    json2typescript_1.JsonObject("Validation")
], Validation);
exports.default = Validation;
//# sourceMappingURL=Validation.js.map