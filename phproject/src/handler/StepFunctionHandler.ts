import {
    DescribeExecutionCommand,
    DescribeStateMachineCommand,
    GetExecutionHistoryCommand,
    StartExecutionCommand,
    StopExecutionCommand
} from "@aws-sdk/client-sfn"

import {
    GetParameterCommand
} from "@aws-sdk/client-ssm"

import AWSSsm from "../utils/AWSSsm"
import AWSStepFunction from "../utils/AWSStepFunction"
import AWSSts from "../utils/AWSSts"
import ObjectUtil from "../utils/ObjectUtil"
import SnowflakeID from "../utils/SnowflakeID"

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

    async startExecution(input: string) {
        const args = JSON.parse(input)
        const params = {
            clusterId: undefined,
            dag_name: args.dag_name,
            parameters: args.parameters,
            iterator: undefined
        }
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const ssmInstance = new AWSSsm(config)
        const ssmCommand = new GetParameterCommand({
            Name: "cluster_id"
        })
        const ssmContent = await ssmInstance.getClient().send(ssmCommand)
        ssmInstance.destroy()
        params.clusterId = ssmContent.Parameter.Value

        if (Array.isArray(args.parameters)) {
            params.iterator = {
                count: args.parameters.length + 1,
                index: 0,
                step: 1
            }
        }

        ObjectUtil.delObjectKeyIsNull(params)

        const stepFunctionInstance = new AWSStepFunction(config)
        const command = new StartExecutionCommand({
            stateMachineArn: "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:" + args.dag_name,
            input: JSON.stringify(params),
            name: `execution_${ new SnowflakeID().nextId() }`
        })
        const stepFunctionContent = await stepFunctionInstance.getClient().send(command)
        stepFunctionInstance.destroy()
        return {
            result: stepFunctionContent,
            input: JSON.stringify(params)
        }

    }

    async stopExecution(arn) {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const instance = new AWSStepFunction(config)
        const client = instance.getClient()
        const command = new StopExecutionCommand({
            executionArn: arn
        })
        await client.send(command)
        instance.destroy()
    }
}
