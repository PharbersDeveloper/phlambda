import {
    DescribeExecutionCommand,
    DescribeStateMachineCommand,
    GetExecutionHistoryCommand
} from "@aws-sdk/client-sfn"

import AWSStepFunction from "../utils/AWSStepFunction"
import AWSSts from "../utils/AWSSts"

export default class StepFunctionHandler {
    async findStepFunctions(arn: string) {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const instance = new AWSStepFunction(config)
        const client = instance.getClient()
        const command = new DescribeStateMachineCommand({
            stateMachineArn: arn
        })
        const content = await client.send(command)
        instance.destroy()
        return content
    }

    async findExecutions(arn: string) {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const instance = new AWSStepFunction(config)
        const client = instance.getClient()
        const command = new DescribeExecutionCommand({
            executionArn: arn
        })
        const content = await client.send(command)
        instance.destroy()
        return content
    }

    async findEventHistory(arn: string) {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const instance = new AWSStepFunction(config)
        const client = instance.getClient()
        const command = new GetExecutionHistoryCommand({
            executionArn: arn,
            reverseOrder: false
        })
        const content = await client.send(command)
        instance.destroy()
        return content
    }
}
