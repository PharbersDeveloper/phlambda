import * as fs from "fs"
import {DBConfig, IStore, Register, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import {AWSRegion, PostgresConf} from "../constants/common"
import StepFunctionHandler from "../handler/StepFunctionHandler"
import AWSSts from "../utils/AWSSts"

const awsConfig = jest.fn(async () => {
    const name = "Ph-Data-Resource-Admin"
    const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey, AWSRegion)
    return await sts.assumeRole(name, `arn:aws-cn:iam::444603803904:role/${name}`)
})

const SNSCreateStepFunctionEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../../events/syncmanger/sns_event.json", "utf8"))
    event.Records[0].Sns.Subject = "functionindex"
    event.Records[0].Sns.Message = JSON.stringify({
        stateMachineArn: "chemdata"
    })
    event.Records[0].Sns.MessageAttributes = {
        action: {
            Type: "String",
            Value: "update"
        },
        type: {
            Type: "String",
            Value: "function"
        }
    }
    return event
})

const SNSDeleteStepFunctionEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../../events/syncmanger/sns_event.json", "utf8"))
    event.Records[0].Sns.Subject = "functionindex"
    event.Records[0].Sns.Message = JSON.stringify({
        stateMachineArn: "chemdata"
    })
    event.Records[0].Sns.MessageAttributes = {
        action: {
            Type: "String",
            Value: "delete"
        },
        type: {
            Type: "String",
            Value: "function"
        }
    }
    return event
})

const SNSUpdateStepFunctionEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../../events/syncmanger/sns_event.json", "utf8"))
    event.Records[0].Sns.Subject = "functionindex"
    event.Records[0].Sns.Message = JSON.stringify({
        stateMachineArn: "chemdata"
    })
    event.Records[0].Sns.MessageAttributes = {
        action: {
            Type: "String",
            Value: "update"
        },
        type: {
            Type: "String",
            Value: "function"
        }
    }
    return event
})

const SNSCreateExecutionEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../../events/syncmanger/sns_event.json", "utf8"))
    event.Records[0].Sns.Subject = "functionindex"
    event.Records[0].Sns.Message = JSON.stringify({
        stateMachineArn: "chemdata",
        executionArn: ""
    })
    event.Records[0].Sns.MessageAttributes = {
        action: {
            Type: "String",
            Value: "create"
        },
        type: {
            Type: "String",
            Value: "execution"
        }
    }
    return event
})

describe("Step Function Test", () => {
    let store: IStore
    let config
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

    // test("Step Function All Index Sync To DB", async () => {
    //     console.time("index")
    //     await store.open()
    //     const handler = new StepFunctionHandler(store, config)
    //     await handler.syncAll()
    //     await store.close()
    //     console.timeEnd("index")
    // }, 1000 * 60 * 100)

    test("SNS Create StepFunction", async () => {
        const event = new SNSCreateStepFunctionEvent()
        await store.open()
        const handler = new StepFunctionHandler(store, config)
        await handler.exec(event)
        await store.close()
    })

    test("SNS Update StepFunction", async () => {
        const event = new SNSUpdateStepFunctionEvent()
        await store.open()
        const handler = new StepFunctionHandler(store, config)
        await handler.exec(event)
        await store.close()
    })

    test("SNS Delete StepFunction", async () => {
        const event = new SNSDeleteStepFunctionEvent()
        await store.open()
        const handler = new StepFunctionHandler(store, config)
        await handler.exec(event)
        await store.close()
    })

    test("SNS Create Execution", async () => {
        const event = new SNSCreateExecutionEvent()
        await store.open()
        const handler = new StepFunctionHandler(store, config)
        await handler.exec(event)
        await store.close()
    })
})

