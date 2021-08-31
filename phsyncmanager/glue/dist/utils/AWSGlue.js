"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const client_glue_1 = require("@aws-sdk/client-glue");
class AWsGlue {
    constructor(config) {
        this.client = null;
        this.client = new client_glue_1.GlueClient(config);
    }
    getClient() {
        return this.client;
    }
    destroy() {
        this.client.destroy();
    }
}
exports.default = AWsGlue;
//# sourceMappingURL=AWSGlue.js.map