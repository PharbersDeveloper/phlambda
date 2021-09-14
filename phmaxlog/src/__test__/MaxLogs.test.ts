import * as fs from "fs"
import {DBConfig, IStore, Register, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import { PostgresConf} from "../constants/common"
import MaxLogHandler from "../handler/MaxLogHandler"

const MaxLogsUpdateEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../../events/syncmanger/sns_event.json", "utf8"))

    event.Records[0].Sns.Subject = "maxlog"
    event.Records[0].Sns.Message = JSON.stringify({
        logId: "twRH_Q-FPFQYSHV6wkLa",
        provider: "ph",
        owner: "001",
        showName: "测试人",
        time: 0,
        version: "",
        code: 0,
        jobDesc: "",
        jobCat: "",
        comments: "",
        message: "",
        date: 0
    })
    event.Records[0].Sns.MessageAttributes = {
        action: {
            Type: "String",
            Value: "update"
        }
    }
    return event
})

describe("Mas Logs Test", () => {
    let config
    let store: IStore
    beforeAll(async () => {
        ServerRegisterConfig([new DBConfig(PostgresConf)])
        store = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
    })

    afterAll(() => {
        store.close()
    })
    test("Log", async () => {
        const event = new MaxLogsUpdateEvent()
        await store.open()
        const handler = new MaxLogHandler(store)
        await handler.exec(event)
        await store.close()
    })
})
