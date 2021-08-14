import {DBConfig, IStore, Register, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import StepFunctionHandler from "../handler/StepFunctionHandler"

process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
process.env.SecretAccessKey = "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"

const configs = [
    new DBConfig({
        name: StoreEnum.POSTGRES,
        entity: "index",
        database: "phentry",
        user: "pharbers",
        password: "Abcde196125",
        host: "127.0.0.1",
        port: 5432,
        poolMax: 2
    })
]
ServerRegisterConfig(configs)
const store = (Register.getInstance.getData(StoreEnum.POSTGRES)) as IStore

describe("Step Function Test", () => {
    test("Step Function All Index Sync To DB", async () => {
        await store.open()
        const handler = new StepFunctionHandler(store)
        await handler.syncAll()
        await store.close()
    }, 1000 * 60 * 100)
})
