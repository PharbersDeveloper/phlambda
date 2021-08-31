"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const client_sfn_1 = require("@aws-sdk/client-sfn");
class AWSStepFunction {
    constructor(config) {
        this.client = null;
        this.client = new client_sfn_1.SFNClient(config);
    }
    getClient() {
        return this.client;
    }
    destroy() {
        this.client.destroy();
    }
}
exports.default = AWSStepFunction;
//# sourceMappingURL=AWSStepFunction.js.map