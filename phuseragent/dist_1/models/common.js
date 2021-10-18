"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class Common {
    constructor() {
        this.model = {
            client: {
                name: String,
                description: String,
                secret: String,
                created: Date,
                modified: Date,
                clientComponents: { link: "component", isArray: true, inverse: "client" }
            },
            component: {
                name: String,
                title: String,
                description: String,
                created: Date,
                modified: Date,
                hbs: String,
                version: String,
                client: { link: "client", isArray: true, inverse: "clientComponents" },
            }
        };
    }
}
exports.default = Common;
//# sourceMappingURL=common.js.map