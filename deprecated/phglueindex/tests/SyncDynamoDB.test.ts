import {DBConfig, IStore, Register, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import {AWSRegion, PostgresConf} from "../src/constants/common"
import SyncGlueHandler from "../src/handler/SyncGlueHandler"
import AWSSts from "../src/utils/AWSSts"

const awsConfig = jest.fn(async (name) => {
    const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey, AWSRegion)
    return await sts.assumeRole(name, `arn:aws-cn:iam::444603803904:role/${name}`)
})

describe("Sync Data 2 DynamoDB", () => {
    let config
    let backRWConfig
    beforeAll(async () => {
        process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
        process.env.SecretAccessKey = "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"

        config = await new awsConfig("Pharbers-ETL-Roles")
        backRWConfig = await new awsConfig("Ph-Back-RW")
    })

    test("Sync Table Partitions 2 DynamoDB", async () => {
        const syncList = [
            {db: "phdatacat", table: "universes"},
            {db: "phdatacat", table: "universe_outlier"},
            {db: "phdatacat", table: "universe_other"},
            {db: "phdatacat", table: "universe_base"},
            {db: "phdatacat", table: "chemdata"},
            {db: "phdatacat", table: "stand_table_by_ma"},
        ]
        console.time("start")
        const handler = new SyncGlueHandler(null, config, backRWConfig)
        for (const item of syncList) {
            await handler.syncPartition2DynamoDB(item.db, item.table)
        }
        console.timeEnd("start")
    })

})
