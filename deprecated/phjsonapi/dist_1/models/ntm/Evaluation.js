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
var Evaluation_1;
"use strict";
const json2typescript_1 = require("json2typescript");
const typegoose_1 = require("typegoose");
const ResultCategory_1 = require("../../enum/ResultCategory");
let Evaluation = Evaluation_1 = class Evaluation extends typegoose_1.Typegoose {
    constructor() {
        super(...arguments);
        this.category = ResultCategory_1.ResultCategory.Overall;
        this.level = "";
        this.abilityDescription = "";
        this.awardDescription = "";
        this.levelDescription = "";
        this.actionDescription = "";
    }
    getModel() {
        return this.getModelForClass(Evaluation_1);
    }
};
__decorate([
    json2typescript_1.JsonProperty("category", String),
    typegoose_1.prop({ enum: ResultCategory_1.ResultCategory, required: true }),
    __metadata("design:type", String)
], Evaluation.prototype, "category", void 0);
__decorate([
    json2typescript_1.JsonProperty("level", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Evaluation.prototype, "level", void 0);
__decorate([
    json2typescript_1.JsonProperty("abilityDescription", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Evaluation.prototype, "abilityDescription", void 0);
__decorate([
    json2typescript_1.JsonProperty("awardDescription", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Evaluation.prototype, "awardDescription", void 0);
__decorate([
    json2typescript_1.JsonProperty("levelDescription", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Evaluation.prototype, "levelDescription", void 0);
__decorate([
    json2typescript_1.JsonProperty("actionDescription", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Evaluation.prototype, "actionDescription", void 0);
Evaluation = Evaluation_1 = __decorate([
    json2typescript_1.JsonObject("Evaluation")
], Evaluation);
exports.default = Evaluation;
//# sourceMappingURL=Evaluation.js.map