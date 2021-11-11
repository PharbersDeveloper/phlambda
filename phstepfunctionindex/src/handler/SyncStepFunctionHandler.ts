import {PutItemCommand} from "@aws-sdk/client-dynamodb"
import {
    DescribeExecutionCommand,
    paginateGetExecutionHistory,
    paginateListExecutions
} from "@aws-sdk/client-sfn"
import {IStore, Logger} from "phnodelayer"
import AWSDynamoDB from "../utils/AWSDynamoDB"
import AWSStepFunction from "../utils/AWSStepFunction"
import ObjectUtil from "../utils/ObjectUtil"
import StepFunctionHandler from "./StepFunctionHandler"

export default class SyncStepFunctionHandler extends StepFunctionHandler {

    private backRWConfig: any
    private stateMap = {
        ExecutionSucceeded: "COMPLETED",
        ExecutionFailed: "FAILED",
        ExecutionAborted: "ABORTED"
    }
    constructor(store: IStore, config: any, backRWConfig: any) {
        super(store, config)
        this.backRWConfig = backRWConfig
    }

    async syncStepFunctionByName(name: string, count: number = -1) {
        const arn = `arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:${name}`
        const executions = []
        const instance = new AWSStepFunction(this.config)
        const client = instance.getClient()
        const sm = await this.store.find("stateMachine", null, {match: { name: arn }})
        const project = await this.store.find("project", this.getRecord(sm).project)
        const stepFunctionsInfo = {
            arn,
            smid: this.getRecord(sm).id,
            owner: this.getRecord(project).owner
        }
        // 接入PG数据库写入stateMachine Index

        // 获取所有StepFunction下的所有Executions
        const pageExecution = await paginateListExecutions({ client }, { stateMachineArn: arn })
        for await (const item of pageExecution) {
            item.executions.forEach((exec) => {
                executions.push({
                    executionArn: exec.executionArn,
                    stateMachineArn: exec.stateMachineArn,
                    smid: stepFunctionsInfo.smid,
                    owner: stepFunctionsInfo.owner
                })
            })
            if (count !== -1 && executions.length >= count) {
                break
            }
        }

        // execution and step 写入DynamoDB
        for (const item of executions) {
            await this.syncExecutions2DynamoDB(item)
            Logger.info("Inert DynamoDB, Execution And Step")
        }
    }

    private getRecord(obj: any) {
        return obj.payload.records[0]
    }

    private async syncExecutions2DynamoDB(execution: any) {
        const instance = new AWSStepFunction(this.config)
        const client = instance.getClient()
        const dyClient = new AWSDynamoDB(this.backRWConfig).getClient()

        const command = new DescribeExecutionCommand({
            executionArn: execution.executionArn
        })
        const content = await client.send(command)

        const pageStepContent = await paginateGetExecutionHistory({ client }, { executionArn: execution.executionArn })
        let stepContents = []
        for await (const item of pageStepContent) {
            item.events.forEach((event) => {
                stepContents.push(JSON.parse(JSON.stringify(event)))
            })
        }
        stepContents = stepContents.filter((event) =>
            event.type === "ExecutionStarted" ||
            event.type === "ExecutionSucceeded" ||
            event.type === "ExecutionFailed" ||
            event.type === "ExecutionAborted"
        )

        const id = ObjectUtil.generateId()
        const dhStepCommand = new PutItemCommand({
            Item: {
                id: {
                    S: id,
                },
                stId: {
                    S: execution.executionArn,
                },
                index: {
                    N: stepContents[0].id.toString()
                },
                input: {
                    S: stepContents[0]?.executionStartedEventDetails?.input || ""
                },
                output: {
                    S: stepContents[1]?.executionSucceededEventDetails?.output || ""
                },
                startTime: {
                    N: new Date(stepContents[0].timestamp).getTime().toString()
                },
                state: {
                    S: this.stateMap[stepContents[1].type] || "UNKNOWN"
                },
                endTime: {
                    N: new Date(stepContents[1].timestamp).getTime().toString()
                },
                stepLog: {
                    S: stepContents[1].type !== "ExecutionFailed" ? "" :
                        stepContents[1].executionFailedEventDetails?.cause
                },
                logLocation: {
                    S: stepContents[1].type !== "ExecutionFailed" ?
                        `ph-platform/2020-11-11/emr/logs/
                        ${JSON.parse(stepContents[1]?.executionSucceededEventDetails?.output || "{}")?.clusterId || ""}/
                        ${JSON.parse(stepContents[1]?.executionSucceededEventDetails?.output || "{}")?.firstStep?.Step?.Id || ""}`
                        : ""
                }
            },
            TableName: "step"
        })

        const dyExecutionCommand = new PutItemCommand({
            Item: {
                id: {
                    S: execution.executionArn
                },
                smId: {
                    S: execution.smid
                },
                input: {
                    S: content.input
                },
                owner: {
                    S: execution.owner
                },
                startTime: {
                    N: content.startDate.getTime().toString()
                },
                state: {
                    S: content.status
                },
                endTime: {
                    N: content.stopDate.getTime().toString()
                },
                steps: {
                    SS: [id]
                },
                type: {
                    S: "stf"
                }
            },
            TableName: "execution"
        })

        await dyClient.send(dhStepCommand)
        await dyClient.send(dyExecutionCommand)
    }
}
