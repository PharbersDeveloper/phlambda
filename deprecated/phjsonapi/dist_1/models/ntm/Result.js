"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const typegoose_1 = require("typegoose");
class Result extends typegoose_1.Typegoose {
    // @prop({ enum: ResultCategory, required: true })
    // public category: ResultCategory
    // @prop({ ref: Level, required: true})
    // public abilityLevel: Ref<Level>
    // @prop({ ref: Level, required: true})
    // public awardLevel: Ref<Level>
    getModel() {
        return this.getModelForClass(Result);
    }
}
exports.default = Result;
//# sourceMappingURL=Result.js.map