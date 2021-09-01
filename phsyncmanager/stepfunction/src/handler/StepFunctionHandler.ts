import {
    DescribeExecutionCommand,
    ListTagsForResourceCommand,
    paginateListExecutions,
    paginateListStateMachines
} from "@aws-sdk/client-sfn"
import { IStore, Logger } from "phnodelayer"
import AWSStepFunction from "../utils/AWSStepFunction"

export default class StepFunctionHandler {

    private readonly store: IStore
    private readonly config: any

    constructor(store: IStore, config: any) {
        this.store = store
        this.config = config
    }

    async exec(event: any) {
        for ( const item of event.Records ) {
            const subject = item?.Sns?.Subject || undefined
            const message = item?.Sns?.Message || undefined
            const attributes = item?.Sns?.MessageAttributes || undefined
            if (message && attributes && subject === "functionindex") {
                switch (attributes.type.Value) {
                    case "function":
                        await this.syncStepFunctions(JSON.parse(message).stateMachineArn, attributes.action.Value)
                        break
                    case "execution":
                        const { stateMachineArn, executionArn, executionId } = JSON.parse(message)
                        await this.syncExecutions(stateMachineArn, executionArn, executionId, attributes.action.Value)
                        break
                }
            }
        }
    }

    async syncAll() {
        const instance = new AWSStepFunction(this.config)
        const client = instance.getClient()
        const stepFunctionContents = await paginateListStateMachines({ client }, {})
        const stepFunctionArns = []
        const executions = []

        // 获取所有StepFunctions的Arn
        for await (const step of stepFunctionContents) {
            for (const item of step.stateMachines) {
                stepFunctionArns.push(item.stateMachineArn)
            }
        }

        // 获取所有StepFunction下的所有Executions
        for (const arn of stepFunctionArns) {
            const pageExecution = await paginateListExecutions({ client }, { stateMachineArn: arn })
            for await (const item of pageExecution) {
                item.executions.forEach((exec) => {
                    executions.push({
                        executionArn: exec.executionArn,
                        stateMachineArn: exec.stateMachineArn
                    })
                })
            }
        }

        // 执行step function index入库操作
        for (const arn of stepFunctionArns) {
            await this.syncStepFunctions(arn, "create")
        }

        // execution index入库操作
        for (const item of executions) {
            await this.syncExecutions(item.stateMachineArn, item.executionArn, "", "create")
        }
    }

    private async syncStepFunctions(arn: string, action: string) {
        const instance = new AWSStepFunction(this.config)
        const client = instance.getClient()
        const tagCommand = new ListTagsForResourceCommand({ resourceArn: arn})
        const tagContent = await client.send(tagCommand)
        switch (action) {
            case "create":
                const record = {
                    arn,
                    name: tagContent.tags.find((item) => item.key === "name")?.value || "unknown",
                    projectName: tagContent.tags.find((item) => item.key === "project")?.value || "unknown",
                    provider: tagContent.tags.find((item) => item.key === "provider")?.value || "unknown",
                    version: tagContent.tags.find((item) => item.key === "version")?.value || "unknown"
                }
                await this.store.create("project", record)
                break
            case "update":
                const project = await this.store.find("project", null, {match: {arn}})
                const updateRecord = {
                    id: project.payload.records[0].id,
                    replace: {
                        name: tagContent.tags.find((item) => item.key === "name")?.value || "unknown",
                        projectName: tagContent.tags.find((item) => item.key === "project")?.value || "unknown",
                        provider: tagContent.tags.find((item) => item.key === "provider")?.value || "unknown",
                        version: tagContent.tags.find((item) => item.key === "version")?.value || "unknown"
                    }
                }
                await this.store.update("project", updateRecord)
                break
            case "delete":
                const dp = await this.store.find("project", null, { match: { arn }})
                await this.store.delete("project", dp.payload.records[0].id)
                await this.store.delete("execution", dp.payload.records[0].executions)
                break
        }
    }

    private async syncExecutions(stateMachineArn: string, executionArn: string, executionId: string, action: string) {
        const instance = new AWSStepFunction(this.config)
        const client = instance.getClient()
        const command = new DescribeExecutionCommand({
            executionArn
        })
        const content = await client.send(command)
        switch (action) {
            case "create":
                const createProject = await this.store.find("project", null, { match: { arn: stateMachineArn }})
                const createRecord = {
                    arn: executionArn,
                    input: content.input,
                    projectExecution: createProject.payload.records[0].id,
                }
                await this.store.create("execution", createRecord)
                break
            case "update":
                const updateRecord = {
                    id: executionId,
                    replace: {
                        arn: executionArn,
                        input: content.input,
                    }
                }
                await this.store.update("execution", updateRecord)
        }
    }
}
