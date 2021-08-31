"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class Max {
    constructor() {
        this.model = {
            project: {
                provider: String,
                time: Number,
                actions: String
            },
            jobLog: {
                provider: String,
                owner: String,
                showName: String,
                time: Number,
                version: String,
                code: Number,
                jobDesc: String,
                jobCat: String,
                comments: String,
                message: String,
                date: Number
            }
        };
        this.operations = {
            hooks: {}
        };
    }
}
exports.default = Max;
//# sourceMappingURL=max.js.map