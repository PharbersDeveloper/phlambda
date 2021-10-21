"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const s3_1 = __importDefault(require("aws-sdk/clients/s3"));
class PhS3Facade {
    constructor() {
        this.s3 = new s3_1.default();
    }
    listBuckets(bkName) {
        return this.s3.listBuckets().promise();
    }
}
exports.default = new PhS3Facade();
//# sourceMappingURL=phS3Facade.js.map