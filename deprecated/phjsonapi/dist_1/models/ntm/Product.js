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
var Product_1;
"use strict";
const json2typescript_1 = require("json2typescript");
const typegoose_1 = require("typegoose");
const Image_1 = __importDefault(require("./Image"));
let Product = Product_1 = class Product extends typegoose_1.Typegoose {
    constructor() {
        super(...arguments);
        this.name = "";
        this.productCategory = "";
        this.medicateCategory = "";
        this.producer = "";
        this.avatarPath = "";
        this.safety = "";
        this.effectiveness = "";
        this.convenience = "";
        this.productType = 0;
        this.priceType = "";
        this.price = 0;
        this.cost = 0;
        this.launchDate = "";
        this.treatmentArea = "";
        this.feature = "";
        this.targetDepartment = "";
        this.patentDescribe = "";
        this.costEffective = "";
        this.lifeCycle = "";
    }
    getModel() {
        return this.getModelForClass(Product_1);
    }
};
__decorate([
    json2typescript_1.JsonProperty("name", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Product.prototype, "name", void 0);
__decorate([
    json2typescript_1.JsonProperty("productCategory", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Product.prototype, "productCategory", void 0);
__decorate([
    json2typescript_1.JsonProperty("medicateCategory", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Product.prototype, "medicateCategory", void 0);
__decorate([
    json2typescript_1.JsonProperty("producer", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Product.prototype, "producer", void 0);
__decorate([
    typegoose_1.prop({ ref: Image_1.default, required: true }),
    __metadata("design:type", Object)
], Product.prototype, "avatar", void 0);
__decorate([
    json2typescript_1.JsonProperty("avatar", String),
    __metadata("design:type", String)
], Product.prototype, "avatarPath", void 0);
__decorate([
    json2typescript_1.JsonProperty("safety", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Product.prototype, "safety", void 0);
__decorate([
    json2typescript_1.JsonProperty("effectiveness", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Product.prototype, "effectiveness", void 0);
__decorate([
    json2typescript_1.JsonProperty("convenience", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Product.prototype, "convenience", void 0);
__decorate([
    json2typescript_1.JsonProperty("productType", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Product.prototype, "productType", void 0);
__decorate([
    json2typescript_1.JsonProperty("priceType", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Product.prototype, "priceType", void 0);
__decorate([
    json2typescript_1.JsonProperty("price", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Product.prototype, "price", void 0);
__decorate([
    json2typescript_1.JsonProperty("cost", Number),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", Number)
], Product.prototype, "cost", void 0);
__decorate([
    json2typescript_1.JsonProperty("launchDate", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Product.prototype, "launchDate", void 0);
__decorate([
    json2typescript_1.JsonProperty("treatmentArea", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Product.prototype, "treatmentArea", void 0);
__decorate([
    json2typescript_1.JsonProperty("feature", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Product.prototype, "feature", void 0);
__decorate([
    json2typescript_1.JsonProperty("targetDepartment", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Product.prototype, "targetDepartment", void 0);
__decorate([
    json2typescript_1.JsonProperty("patentDescribe", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Product.prototype, "patentDescribe", void 0);
__decorate([
    json2typescript_1.JsonProperty("costEffective", String),
    typegoose_1.prop({ required: false, default: "" }),
    __metadata("design:type", String)
], Product.prototype, "costEffective", void 0);
__decorate([
    json2typescript_1.JsonProperty("lifeCycle", String),
    typegoose_1.prop({ required: true }),
    __metadata("design:type", String)
], Product.prototype, "lifeCycle", void 0);
Product = Product_1 = __decorate([
    json2typescript_1.JsonObject("Product")
], Product);
exports.default = Product;
//# sourceMappingURL=Product.js.map