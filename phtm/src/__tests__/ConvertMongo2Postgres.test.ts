import * as fs from "fs"

import { ConfigRegistered, JsonApiMain, Logger, MongoConfig, PostgresConfig, SF, Store } from "phnodelayer"
import {PostgresqlConf} from "../common/config"

const convert2JsonApi = (type: string, record: any) => {
    // delete record.id
    return {
        data: {
            type,
            attributes: record
        }
    }
}

const jsonApiPost = jest.fn((type: string, body: string) => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_post.json", "utf8"))
    event.pathParameters.type = type
    event.path = `${event.path}/${type}`
    event.body = body
    return event
})

describe("convert mongodb 2 postgresql",  () => {
    // 只有转换数据才解开注释

    const app = require("../../app.js")
    let mdb = null
    beforeEach(async () => {
        Logger.debug("before......")
        const conf = new MongoConfig("mongodb", "mongo", "", "", "localhost", 27017, "pharbers-tm")
        const postgresConf = new PostgresConfig(PostgresqlConf.entry, PostgresqlConf.user,
            PostgresqlConf.password, PostgresqlConf.url,
            PostgresqlConf.port, PostgresqlConf.db)
        ConfigRegistered.getInstance.registered(conf).registered(postgresConf)
        mdb = SF.getInstance.get(Store.Mongo)
        await mdb.open()
    })
    afterEach(async () => {
        Logger.debug("after......")
        await mdb.close()
    })

    // test("convert evaluation 2 postgresql", async () => {
    //     Logger.debug("Run ......")
    //     const eveResult = await mdb.find("evaluation", null)
    //     for (const item of eveResult.payload.records) {
    //         const record = convert2JsonApi("evaluations", item)
    //         const result = await app.lambdaHandler(new jsonApiPost("evaluations", JSON.stringify(record)), undefined)
    //         expect(result.statusCode).toBe(201)
    //     }
    // }, 1000 * 60 * 100)
    //
    // test("convert image 2 postgresql", async () => {
    //     Logger.debug("Run ......")
    //     const eveResult = await mdb.find("image", null)
    //     for (const item of eveResult.payload.records) {
    //         const record = convert2JsonApi("images", item)
    //         const result = await app.lambdaHandler(new jsonApiPost("images", JSON.stringify(record)), undefined)
    //         expect(result.statusCode).toBe(201)
    //     }
    // }, 1000 * 60 * 100)
    //
    // test("convert hospital 2 postgresql", async () => {
    //     Logger.debug("Run ......")
    //     const eveResult = await mdb.find("hospital", null)
    //     for (const item of eveResult.payload.records) {
    //         const record = convert2JsonApi("hospitals", item)
    //         const result = await app.lambdaHandler(new jsonApiPost("hospitals", JSON.stringify(record)), undefined)
    //         expect(result.statusCode).toBe(201)
    //     }
    // }, 1000 * 60 * 100)
    //
    // test("convert product 2 postgresql", async () => {
    //     Logger.debug("Run ......")
    //     const eveResult = await mdb.find("product", null)
    //     for (const item of eveResult.payload.records) {
    //         const record = convert2JsonApi("products", item)
    //         const result = await app.lambdaHandler(new jsonApiPost("products", JSON.stringify(record)), undefined)
    //         expect(result.statusCode).toBe(201)
    //     }
    // }, 1000 * 60 * 100)
    //
    // test("convert resource 2 postgresql", async () => {
    //     Logger.debug("Run ......")
    //     const eveResult = await mdb.find("resource", null)
    //     for (const item of eveResult.payload.records) {
    //         const record = convert2JsonApi("resources", item)
    //         const result = await app.lambdaHandler(new jsonApiPost("resources", JSON.stringify(record)), undefined)
    //         expect(result.statusCode).toBe(201)
    //     }
    // }, 1000 * 60 * 100)
    //
    // test("convert requirement 2 postgresql", async () => {
    //     Logger.debug("Run ......")
    //     const eveResult = await mdb.find("requirement", null)
    //     for (const item of eveResult.payload.records) {
    //         const record = convert2JsonApi("requirements", item)
    //         const result = await app.lambdaHandler(new jsonApiPost("requirements", JSON.stringify(record)), undefined)
    //         expect(result.statusCode).toBe(201)
    //     }
    // }, 1000 * 60 * 100)
    //
    // test("convert report 2 postgresql", async () => {
    //     Logger.debug("Run ......")
    //     const eveResult = await mdb.find("report", null)
    //     for (const item of eveResult.payload.records) {
    //         const record = convert2JsonApi("reports", item)
    //         const result = await app.lambdaHandler(new jsonApiPost("reports", JSON.stringify(record)), undefined)
    //         expect(result.statusCode).toBe(201)
    //     }
    // }, 1000 * 60 * 100)
    //
    // test("convert proposal 2 postgresql", async () => {
    //     Logger.debug("Run ......")
    //     const eveResult = await mdb.find("proposal", null)
    //     for (const item of eveResult.payload.records) {
    //         const record = convert2JsonApi("proposals", item)
    //         const result = await app.lambdaHandler(new jsonApiPost("proposals", JSON.stringify(record)), undefined)
    //         expect(result.statusCode).toBe(201)
    //     }
    // }, 1000 * 60 * 100)
    //
    // test("convert preset 2 postgresql", async () => {
    //     Logger.debug("Run ......")
    //     const eveResult = await mdb.find("preset", null)
    //     for (const item of eveResult.payload.records) {
    //         const record = convert2JsonApi("presets", item)
    //         const result = await app.lambdaHandler(new jsonApiPost("presets", JSON.stringify(record)), undefined)
    //         expect(result.statusCode).toBe(201)
    //     }
    // }, 1000 * 60 * 100)
    //
    // test("convert usableProposal 2 postgresql", async () => {
    //     Logger.debug("Run ......")
    //     const eveResult = await mdb.find("usableProposal", null)
    //     for (const item of eveResult.payload.records) {
    //         const record = convert2JsonApi("usable-proposals", item)
    //         const result = await app.lambdaHandler(new jsonApiPost("usable-proposals",
    //             JSON.stringify(record)), undefined)
    //         expect(result.statusCode).toBe(201)
    //     }
    // }, 1000 * 60 * 100)

    test("temp", () => {
        Logger.info("请忽视我")
    })

})
