import { DeleteItemCommand, QueryCommand, ScanCommand } from "@aws-sdk/client-dynamodb"
import {AWSRegion} from "../src/constants/common"
import AWSDynamoDB from "../src/utils/AWSDynamoDB"
import AWSSts from "../src/utils/AWSSts"

const awsConfig = jest.fn(async (name) => {
    const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey, AWSRegion)
    return await sts.assumeRole(name, `arn:aws-cn:iam::444603803904:role/${name}`)
})

describe("delete step and execution", () => {
    let backRWConfig
    let steps
    let executions
    beforeAll(async () => {
        process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
        process.env.SecretAccessKey = "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"
        backRWConfig = await new awsConfig("Ph-Back-RW")

        const dyClient = new AWSDynamoDB(backRWConfig).getClient()
        const stepCmd = new ScanCommand({
            TableName: "step"
        })
        const executionCmd = new ScanCommand({
            TableName: "execution"
        })
        steps = (await dyClient.send(stepCmd)).Items.map((item) => {
            return {
                id: item.id,
                stId: item.stId
            }
        })
        executions = (await dyClient.send(executionCmd)).Items.map((item) => {
            return {
                id: item.id,
                smId: item.smId
            }
        })
    })

    test("step", async () => {
        const dyClient = new AWSDynamoDB(backRWConfig).getClient()
        for (const item of steps) {
            const command = new DeleteItemCommand({
                TableName: "step",
                Key: {
                    id: item.id,
                    stId: item.stId
                }
            })
            await dyClient.send(command)
        }
    })

    test("execution", async () => {
        const dyClient = new AWSDynamoDB(backRWConfig).getClient()
        for (const item of executions) {
            const command = new DeleteItemCommand({
                TableName: "execution",
                Key: {
                    id: item.id,
                    smId: item.smId
                }
            })
            await dyClient.send(command)
        }
    })
})
