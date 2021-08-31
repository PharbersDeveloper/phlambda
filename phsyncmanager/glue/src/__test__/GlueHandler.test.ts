import * as fs from "fs"
import {DBConfig, IStore, Register, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import {AWSRegion, PostgresConf} from "../constants/common"
import GlueHandler from "../handler/GlueHandler"
import AWSSts from "../utils/AWSSts"

const awsConfig = jest.fn(async () => {
    const name = "Pharbers-ETL-Roles"
    const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey, AWSRegion)
    return await sts.assumeRole(name, `arn:aws-cn:iam::444603803904:role/${name}`)
})

const SNSUpdateTableEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../../events/syncmanger/glue/sns_event.json", "utf8"))
    event.Records[0].Sns.Subject = "glue"
    event.Records[0].Sns.Message = JSON.stringify({
        name: "chemdata",
        database: "phdatacat"
    })
    event.Records[0].Sns.MessageAttributes = {
        action: {
            Type: "String",
            Value: "update"
        },
        type: {
            Type: "String",
            Value: "table"
        }
    }
    return event
})

const SNSDeleteDataBaseEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../../events/syncmanger/glue/sns_event.json", "utf8"))
    event.Records[0].Sns.Subject = "glue"
    event.Records[0].Sns.Message = JSON.stringify({
        name: "phdatacat",
    })
    event.Records[0].Sns.MessageAttributes = {
        action: {
            Type: "String",
            Value: "delete"
        },
        type: {
            Type: "String",
            Value: "database"
        }
    }
    return event
})

describe("Glue Test", () => {
    let config
    let store: IStore
    beforeAll(async () => {
        process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
        process.env.SecretAccessKey = "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"
        config = await new awsConfig()
        ServerRegisterConfig([new DBConfig(PostgresConf)])
        store = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
    })

    afterAll(() => {
        store.close()
    })

    // test("SNS Update Glue Table Event", async () => {
    //     const event = new SNSUpdateTableEvent()
    //     await store.open()
    //     const handler = new GlueHandler(store, config)
    //     await handler.exec(event)
    //     await store.close()
    // })

    test("SNS Delete Glue DataBase", async () => {
        const event = new SNSDeleteDataBaseEvent()
        await store.open()
        const handler = new GlueHandler(store, config)
        await handler.exec(event)
        await store.close()
    })
})
