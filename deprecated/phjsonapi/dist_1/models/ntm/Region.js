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
var Region_1;
"use strict";
const json2typescript_1 = require("json2typescript");
const typegoose_1 = require("typegoose");
let Region = Region_1 = class Region extends typegoose_1.Typegoose {
    constructor() {
        super(...arguments);
        this.name = "";
        this.level = "";
        this.strategyPosition = "";
        this.localPatient = 0.0;
        this.outsidePatient = 0.0;
        this.patientNum = 0.0;
    }
    getModel() {
        return this.getModelForClass(Region_1);
    }
};
__decorate([
    json2typescript_1.JsonProperty("name", String),
    typegoose_1.prop({ required: true, default: "" }),
    __metadata("design:type", String)
], Region.prototype, "name", void 0);
__decorate([
    json2typescript_1.JsonProperty("level", String),
    typegoose_1.prop({ required: true, default: "" }),
    __metadata("design:type", String)
], Region.prototype, "level", void 0);
__decorate([
    json2typescript_1.JsonProperty("strategyPosition", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Region.prototype, "strategyPosition", void 0);
__decorate([
    json2typescript_1.JsonProperty("localPatient", Number),
    typegoose_1.prop({ required: true, default: 0.0 }),
    __metadata("design:type", Number)
], Region.prototype, "localPatient", void 0);
__decorate([
    json2typescript_1.JsonProperty("outsidePatient", Number),
    typegoose_1.prop({ required: true, default: 0.0 }),
    __metadata("design:type", Number)
], Region.prototype, "outsidePatient", void 0);
__decorate([
    json2typescript_1.JsonProperty("patientNum", Number),
    typegoose_1.prop({ required: true, default: 0.0 }),
    __metadata("design:type", Number)
], Region.prototype, "patientNum", void 0);
Region = Region_1 = __decorate([
    json2typescript_1.JsonObject("Evaluation")
], Region);
exports.default = Region;
//# sourceMappingURL=Region.js.map