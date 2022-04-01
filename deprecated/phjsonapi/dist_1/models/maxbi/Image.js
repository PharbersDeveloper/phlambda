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
var Image_1;
"use strict";
const json2typescript_1 = require("json2typescript");
const typegoose_1 = require("typegoose");
let Image = Image_1 = class Image extends typegoose_1.Typegoose {
    constructor() {
        super(...arguments);
        this.img = "";
        this.alt = "";
        this.tag = "";
        this.flag = 0;
    }
    getModel() {
        return this.getModelForClass(Image_1);
    }
};
__decorate([
    json2typescript_1.JsonProperty("img", String),
    typegoose_1.prop({ required: true, default: "" }),
    __metadata("design:type", String)
], Image.prototype, "img", void 0);
__decorate([
    json2typescript_1.JsonProperty("alt", String),
    typegoose_1.prop({ required: true, default: "" }),
    __metadata("design:type", String)
], Image.prototype, "alt", void 0);
__decorate([
    json2typescript_1.JsonProperty("tag", String),
    typegoose_1.prop({ required: true, default: "" }),
    __metadata("design:type", String)
], Image.prototype, "tag", void 0);
__decorate([
    json2typescript_1.JsonProperty("flag", Number),
    typegoose_1.prop({ required: true, default: 0 }),
    __metadata("design:type", Number)
], Image.prototype, "flag", void 0);
Image = Image_1 = __decorate([
    json2typescript_1.JsonObject("Image")
], Image);
exports.default = Image;
//# sourceMappingURL=Image.js.map