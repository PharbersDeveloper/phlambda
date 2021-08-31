"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs = __importStar(require("fs"));
const phnodelayer_1 = require("phnodelayer");
const common_1 = require("../constants/common");
const GlueHandler_1 = __importDefault(require("../handler/GlueHandler"));
const AWSSts_1 = __importDefault(require("../utils/AWSSts"));
const awsConfig = jest.fn(async () => {
    const name = "Pharbers-ETL-Roles";
    const sts = new AWSSts_1.default(process.env.AccessKeyId, process.env.SecretAccessKey, common_1.AWSRegion);
    return await sts.assumeRole(name, `arn:aws-cn:iam::444603803904:role/${name}`);
});
const SNSUpdateTableEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../../events/syncmanger/glue/sns_event.json", "utf8"));
    event.Records[0].Sns.Subject = "glue";
    event.Records[0].Sns.Message = JSON.stringify({
        name: "chemdata",
        database: "phdatacat"
    });
    event.Records[0].Sns.MessageAttributes = {
        action: {
            Type: "String",
            Value: "update"
        },
        type: {
            Type: "String",
            Value: "table"
        }
    };
    return event;
});
const SNSDeleteDataBaseEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../../events/syncmanger/glue/sns_event.json", "utf8"));
    event.Records[0].Sns.Subject = "glue";
    event.Records[0].Sns.Message = JSON.stringify({
        name: "phdatacat",
    });
    event.Records[0].Sns.MessageAttributes = {
        action: {
            Type: "String",
            Value: "delete"
        },
        type: {
            Type: "String",
            Value: "database"
        }
    };
    return event;
});
describe("Glue Test", () => {
    let config;
    let store;
    beforeAll(async () => {
        process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX";
        process.env.SecretAccessKey = "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";
        config = await new awsConfig();
        phnodelayer_1.ServerRegisterConfig([new phnodelayer_1.DBConfig(common_1.PostgresConf)]);
        store = phnodelayer_1.Register.getInstance.getData(phnodelayer_1.StoreEnum.POSTGRES);
    });
    afterAll(() => {
        store.close();
    });
    // test("SNS Update Glue Table Event", async () => {
    //     const event = new SNSUpdateTableEvent()
    //     await store.open()
    //     const handler = new GlueHandler(store, config)
    //     await handler.exec(event)
    //     await store.close()
    // })
    test("SNS Delete Glue DataBase", async () => {
        const event = new SNSDeleteDataBaseEvent();
        await store.open();
        const handler = new GlueHandler_1.default(store, config);
        await handler.exec(event);
        await store.close();
    });
});
//# sourceMappingURL=GlueHandler.test.js.map