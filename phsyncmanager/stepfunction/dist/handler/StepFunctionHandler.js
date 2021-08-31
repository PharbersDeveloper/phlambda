"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const client_sfn_1 = require("@aws-sdk/client-sfn");
const AWSStepFunction_1 = __importDefault(require("../utils/AWSStepFunction"));
class StepFunctionHandler {
    constructor(store, config) {
        this.store = store;
        this.config = config;
    }
    async exec(event) {
        for (const item of event.Records) {
            const subject = item?.Sns?.Subject || undefined;
            const message = item?.Sns?.Message || undefined;
            const attributes = item?.Sns?.MessageAttributes || undefined;
            if (message && attributes && subject === "functionindex") {
                switch (attributes.type.Value) {
                    case "function":
                        await this.syncStepFunctions(JSON.parse(message).stateMachineArn, attributes.action.Value);
                        break;
                    case "execution":
                        const { stateMachineArn, executionArn } = JSON.parse(message);
                        await this.syncExecutions(stateMachineArn, executionArn, attributes.action.Value);
                        break;
                }
            }
        }
    }
    async syncAll() {
        const instance = new AWSStepFunction_1.default(this.config);
        const client = instance.getClient();
        const stepFunctionContents = await client_sfn_1.paginateListStateMachines({ client }, {});
        const stepFunctionArns = [];
        const executions = [];
        // 获取所有StepFunctions的Arn
        for await (const step of stepFunctionContents) {
            for (const item of step.stateMachines) {
                stepFunctionArns.push(item.stateMachineArn);
            }
        }
        // 获取所有StepFunction下的所有Executions
        for (const arn of stepFunctionArns) {
            const pageExecution = await client_sfn_1.paginateListExecutions({ client }, { stateMachineArn: arn });
            for await (const item of pageExecution) {
                item.executions.forEach((exec) => {
                    executions.push({
                        executionArn: exec.executionArn,
                        stateMachineArn: exec.stateMachineArn
                    });
                });
            }
        }
        // 执行step function index入库操作
        for (const arn of stepFunctionArns) {
            await this.syncStepFunctions(arn, "create");
        }
        // execution index入库操作
        for (const item of executions) {
            await this.syncExecutions(item.stateMachineArn, item.executionArn, "create");
        }
    }
    async syncStepFunctions(arn, action) {
        const instance = new AWSStepFunction_1.default(this.config);
        const client = instance.getClient();
        const tagCommand = new client_sfn_1.ListTagsForResourceCommand({ resourceArn: arn });
        const tagContent = await client.send(tagCommand);
        switch (action) {
            case "create":
                const record = {
                    arn,
                    name: tagContent.tags.find((item) => item.key === "name")?.value || "unknown",
                    projectName: tagContent.tags.find((item) => item.key === "project")?.value || "unknown",
                    provider: tagContent.tags.find((item) => item.key === "provider")?.value || "unknown",
                    version: tagContent.tags.find((item) => item.key === "version")?.value || "unknown"
                };
                await this.store.create("project", record);
                break;
            case "update":
                const project = await this.store.find("project", null, { match: { arn } });
                const updateRecord = {
                    id: project.payload.records[0].id,
                    replace: {
                        name: tagContent.tags.find((item) => item.key === "name")?.value || "unknown",
                        projectName: tagContent.tags.find((item) => item.key === "project")?.value || "unknown",
                        provider: tagContent.tags.find((item) => item.key === "provider")?.value || "unknown",
                        version: tagContent.tags.find((item) => item.key === "version")?.value || "unknown"
                    }
                };
                await this.store.update("project", updateRecord);
                break;
            case "delete":
                const dp = await this.store.find("project", null, { match: { arn } });
                await this.store.delete("project", dp.payload.records[0].id);
                await this.store.delete("execution", dp.payload.records[0].executions);
                break;
        }
    }
    async syncExecutions(stateMachineArn, executionArn, action) {
        const instance = new AWSStepFunction_1.default(this.config);
        const client = instance.getClient();
        const command = new client_sfn_1.DescribeExecutionCommand({
            executionArn
        });
        const content = await client.send(command);
        switch (action) {
            case "create":
                const project = await this.store.find("project", null, { match: { arn: stateMachineArn } });
                const record = {
                    arn: executionArn,
                    input: content.input,
                    projectExecution: project.payload.records[0].id,
                };
                await this.store.create("execution", record);
                break;
        }
    }
}
exports.default = StepFunctionHandler;
//# sourceMappingURL=StepFunctionHandler.js.map