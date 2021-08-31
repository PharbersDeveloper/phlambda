"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class Index {
    constructor() {
        this.model = {
            project: {
                arn: String,
                name: String,
                projectName: String,
                provider: String,
                version: String,
                executions: { link: "execution", isArray: true, inverse: "projectExecution" }
            },
            execution: {
                projectExecution: { link: "project", inverse: "executions" },
                arn: String,
                input: String,
            },
        };
        this.operations = {
            hooks: {}
        };
    }
}
exports.default = Index;
//# sourceMappingURL=index.js.map