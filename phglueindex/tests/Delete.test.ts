import { DeleteItemCommand, QueryCommand, ScanCommand } from "@aws-sdk/client-dynamodb"
import {AWSRegion} from "../src/constants/common"
import AWSDynamoDB from "../src/utils/AWSDynamoDB"
import AWSSts from "../src/utils/AWSSts"

const awsConfig = jest.fn(async (name) => {
    const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey, AWSRegion)
    return await sts.assumeRole(name, `arn:aws-cn:iam::444603803904:role/${name}`)
})

describe("delete partition", () => {
    let backRWConfig
    let partition
    beforeAll(async () => {
        process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
        process.env.SecretAccessKey = "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"
        backRWConfig = await new awsConfig("Ph-Back-RW")

        const dyClient = new AWSDynamoDB(backRWConfig).getClient()
        const stepCmd = new ScanCommand({
            TableName: "partition"
        })
        partition = (await dyClient.send(stepCmd)).Items.map((item) => {
            return {
                id: item.id,
                smID: item.smID
            }
        })
    })

    test("partition", async () => {
        const dyClient = new AWSDynamoDB(backRWConfig).getClient()
        for (const item of partition) {
            const command = new DeleteItemCommand({
                TableName: "partition",
                Key: {
                    id: item.id,
                    smID: item.smID
                }
            })
            await dyClient.send(command)
        }
    })
})
