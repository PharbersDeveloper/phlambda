"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const AWS = require("aws-sdk");
AWS.config.update({ region: "cn-northwest-1" });
class PhS3Facade {
    constructor() {
        this.s3 = new AWS.S3({ apiVersion: "2006-03-01" });
    }
    listBuckets(bkName) {
        return __awaiter(this, void 0, void 0, function* () {
            return this.s3.listBuckets().promise();
        });
    }
    getObject(bkName, key) {
        return __awaiter(this, void 0, void 0, function* () {
            const result = yield this.s3.getObject({ Bucket: bkName, Key: key }).promise();
            return result.Body;
        });
    }
}
exports.default = new PhS3Facade();
//# sourceMappingURL=phS3Facade.js.map