import {DBConfig, IStore, Register, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import AWSConfig from "../common/AWSConfig"
import GlueHandler from "../handler/GlueHandler"

process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
process.env.SecretAccessKey = "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"

const configs = [
    new DBConfig({
        name: StoreEnum.POSTGRES,
        entity: "index",
        database: "phentry",
        user: "pharbers",
        password: "Abcde196125",
        host: "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn",
        port: 5432,
        poolMax: 2
    })
]
ServerRegisterConfig(configs)
const store = (Register.getInstance.getData(StoreEnum.POSTGRES)) as IStore

describe("Glue Test", () => {
    test("Glue All Index Sync To DB", async () => {

        const awsConfigs = ["Ph-Data-Resource-Admin", "Pharbers-ETL-Roles"]
        const awsConfig = AWSConfig.getInstance
        await awsConfig.register(awsConfigs)

        console.time("index")
        await store.open()
        const handler = new GlueHandler(store)
        await handler.syncAll()
        await store.close()
        console.timeEnd("index")
    }, 1000 * 60 * 100)

    test("Glue Partition Count", async () => {
        const awsConfigs = ["Ph-Data-Resource-Admin", "Pharbers-ETL-Roles"]
        const awsConfig = AWSConfig.getInstance
        await awsConfig.register(awsConfigs)

        const handler = new GlueHandler(store)
        await handler.syncAll(true)

    }, 1000 * 60 * 20)
})
