import {
    DescribeExecutionCommand,
    // DescribeStateMachineCommand,
    ListTagsForResourceCommand,
    paginateListExecutions,
    paginateListStateMachines
} from "@aws-sdk/client-sfn"
import { IStore, Logger, Register, StoreEnum } from "phnodelayer"
import AWSStepFunction from "../utils/AWSStepFunction"
import AWSSts from "../utils/AWSSts"

export default class StepFunctionHandler {

    private readonly store: IStore

    constructor(store: IStore) {
        this.store = store
    }

    async exec(event: any) {
        Logger.info("exec")
    }

    async syncAll() {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const instance = new AWSStepFunction(config)
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
        // for (const arn of stepFunctionArns) {
        //     await this.syncStepFunctions(arn)
        // }

        // execution index入库操作
        // for (const item of executions) {
        //     await this.syncExecutions(item.stateMachineArn, item.executionArn)
        // }

        console.info(stepFunctionArns.length)
        console.info(executions.length)
    }

    private async syncStepFunctions(arn: string) {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const instance = new AWSStepFunction(config)
        const client = instance.getClient()
        // const command = new DescribeStateMachineCommand({ stateMachineArn: arn })
        // const content = await client.send(command)
        const tagCommand = new ListTagsForResourceCommand({ resourceArn: arn})
        const tagContent = await client.send(tagCommand)
        instance.destroy()
        const record = {
            arn,
            name: tagContent.tags.find((item) => item.key === "name")?.value || "unknown",
            provider: tagContent.tags.find((item) => item.key === "provider")?.value || "unknown",
            version: tagContent.tags.find((item) => item.key === "version")?.value || "unknown"
        }
        await this.store.create("project", record)
    }

    private async syncExecutions(stateMachineArn: string, executionArn: string) {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const instance = new AWSStepFunction(config)
        const client = instance.getClient()
        const command = new DescribeExecutionCommand({
            executionArn
        })
        const content = await client.send(command)
        instance.destroy()
        const project = await this.store.find("project", null, { match: { arn: stateMachineArn }})
        const record = {
            arn: executionArn,
            input: content.input,
            projectExecution: project.payload.records[0].id,
        }
        await this.store.create("execution", record)
        // console.info(record)
    }
}
