import {DBConfig, IStore, Register, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import {AWSRegion, PostgresConf} from "../src/constants/common"
import SyncStepFunctionHandler from "../src/handler/SyncStepFunctionHandler"
import AWSSts from "../src/utils/AWSSts"

const awsConfig = jest.fn(async (name) => {
    const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey, AWSRegion)
    return await sts.assumeRole(name, `arn:aws-cn:iam::444603803904:role/${name}`)
})

describe("Sync Data 2 DynamoDB", () => {
    let store: IStore
    let config
    let backRWConfig
    beforeAll(async () => {
        process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
        process.env.SecretAccessKey = "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"

        config = await new awsConfig("Ph-Data-Resource-Admin")
        backRWConfig = await new awsConfig("Ph-Back-RW")

        ServerRegisterConfig([new DBConfig(PostgresConf)])
        store = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
        await store.open()
    })

    afterAll(async () => {
        await store.close()
    })

    test("sync ETL_Iterator execution and step", async () => {
        console.time("ETL_Iterator")
        const handler = new SyncStepFunctionHandler(store, config, backRWConfig)
        await handler.syncStepFunctionByName("ETL_Iterator", 100)
        console.timeEnd("ETL_Iterator")
    })

    test("sync Auto_max_refactor execution and step", async () => {
        console.time("Auto_max_refactor")
        const handler = new SyncStepFunctionHandler(store, config, backRWConfig)
        await handler.syncStepFunctionByName("Auto_max_refactor", 100)
        console.timeEnd("Auto_max_refactor")
    })
})
