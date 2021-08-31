"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class Index {
    constructor() {
        this.model = {
            db: {
                name: String,
                provider: String,
                tables: { link: "table", isArray: true, inverse: "db" },
            },
            table: {
                name: String,
                database: String,
                provider: String,
                version: String,
                db: { link: "db", inverse: "tables" },
            }
        };
        this.operations = {
            hooks: {}
        };
    }
}
exports.default = Index;
//# sourceMappingURL=index.js.map