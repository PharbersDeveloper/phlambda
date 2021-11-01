import * as fs from "fs"
import {DBConfig, IStore, Register, ServerRegisterConfig, StoreEnum} from "phnodelayer"
import {AWSRegion, PostgresConf} from "../src/constants/common"
import StepFunctionHandler from "../src/handler/StepFunctionHandler"
import AWSSts from "../src/utils/AWSSts"

const awsConfig = jest.fn(async (name) => {
    const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey, AWSRegion)
    return await sts.assumeRole(name, `arn:aws-cn:iam::444603803904:role/${name}`)
})

const SNSCreateStepFunctionEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("events/sns_event.json", "utf8"))
    event.Records[0].Sns.Subject = "functionindex"
    event.Records[0].Sns.Message = JSON.stringify({
        stateMachineArn: "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:ETL_Iterator"
    })
    event.Records[0].Sns.MessageAttributes = {
        action: {
            Type: "String",
            Value: "create"
        },
        type: {
            Type: "String",
            Value: "function"
        }
    }
    return event
})

const SNSDeleteStepFunctionEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("events/sns_event.json", "utf8"))
    event.Records[0].Sns.Subject = "functionindex"
    event.Records[0].Sns.Message = JSON.stringify({
        stateMachineArn: "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:ETL_Iterator"
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
    const event = JSON.parse(fs.readFileSync("events/sns_event.json", "utf8"))
    event.Records[0].Sns.Subject = "functionindex"
    event.Records[0].Sns.Message = JSON.stringify({
        stateMachineArn: "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:ETL_Iterator"
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
    const event = JSON.parse(fs.readFileSync("events/sns_event.json", "utf8"))
    event.Records[0].Sns.Subject = "functionindex"
    event.Records[0].Sns.Message = JSON.stringify({
        stateMachineArn: "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:ETL_Iterator",
        executionArn: "arn:aws-cn:states:cn-northwest-1:444603803904:execution:ETL_Iterator:execution_334950027216687104"
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

const SNSUpdateExecutionEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("events/sns_event.json", "utf8"))
    event.Records[0].Sns.Subject = "functionindex"
    event.Records[0].Sns.Message = JSON.stringify({
        stateMachineArn: "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:ETL_Iterator",
        executionArn: "arn:aws-cn:states:cn-northwest-1:444603803904:execution:ETL_Iterator:execution_334950027216687104",
        executionId: "PgcZbvHIW2_Uq5TnCwBy"
    })
    event.Records[0].Sns.MessageAttributes = {
        action: {
            Type: "String",
            Value: "update"
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

        config = await new awsConfig("Ph-Data-Resource-Admin")

        ServerRegisterConfig([new DBConfig(PostgresConf)])
        store = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
    })

    afterAll(() => {
        store.close()
    })

    test("Step Function All Index Sync To DB", async () => {
        console.time("index")
        await store.open()
        const handler = new StepFunctionHandler(store, config)
        await handler.syncAll()
        await store.close()
        console.timeEnd("index")
    })

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

    test("SNS Create Execution", async () => {
        const event = new SNSCreateExecutionEvent()
        await store.open()
        const handler = new StepFunctionHandler(store, config)
        await handler.exec(event)
        await store.close()
    })

    test("SNS Update Execution", async () => {
        const event = new SNSUpdateExecutionEvent()
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
})
