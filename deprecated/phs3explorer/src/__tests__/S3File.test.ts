import * as fs from "fs"
import S3Handler from "../handler/S3Handler"

const CreateUploadJobLog = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/phs3explorer/event_create_log.json", "utf8"))
    event.body = JSON.stringify({
        data: {
            type: "job-logs",
            attributes: {
                provider: "UCB",
                owner: "5UBSLZvV0w9zh7-lZQap",
                showName: "钱鹏",
                version: "测试表.xlsx",
                code: 0,
                jobDesc: "success",
                jobCat: "upload",
                comments: "测试数据",
                message: JSON.stringify(
                    {
                        tags: [
                            {Key: "name", Value: "Alex"}
                        ],
                        asset: {
                            fileName: "测试表",
                            extension: "xlsx",
                            size: 1000,
                            labels: [],
                            description: "测试表",
                            type: "file",
                        },
                        tempfile: "00001.xlsx"
                    }
                ),
                date: 1629869854734,
                time: 1617206400000
            }
        }
    })
    return event
})

const CreateMapperJobLog = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/phs3explorer/event_create_log.json", "utf8"))
    event.body = JSON.stringify({
        data: {
            type: "job-logs",
            id: "00011",
            attributes: {
                provider: "UCB",
                owner: "5UBSLZvV0w9zh7-lZQap",
                showName: "钱鹏",
                version: "测试表.xlsx",
                code: 0,
                jobDesc: "success",
                jobCat: "mapper",
                comments: "测试数据",
                message: JSON.stringify(
                    {
                        tags: [
                            {Key: "mapper", Value: "00011"}
                        ],
                        tempfile: "00001.xlsx",
                        mapper: [
                            {key: "value"}
                        ]
                    }
                ),
                date: 1629869854734,
                time: 1617206400000
            }
        }
    })
    return event
})

const CreateETL = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/phs3explorer/event_etl.json", "utf8"))
})

describe("S3 Tags", () => {
    beforeAll(async () => {
        process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
        process.env.SecretAccessKey = "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"
        process.env.PATH_PREFIX = "/Users/qianpeng/Desktop/"
    })

    test("Put File And Put Upload Tags", async () => {
        function sleep(ms) {
            return new Promise((resolve) => setTimeout(resolve, ms))
        }
        console.time("a")
        const bucket = "ph-origin-files"
        const key = "user/测试表.xlsx"
        const path = "/Users/qianpeng/Desktop/测试表.xlsx"
        const tags = [
            {
                Key: "name",
                Value: "Alex"
            },
            {
                Key: "mapper",
                Value: "1"
            }
        ].map(( item ) => `${item.Key}=${item.Value}`).join("&")
        const s3 = new S3Handler()
        await s3.putFile(bucket, key, path, tags)
        console.timeEnd("a")
    }, 1000 * 60 * 10)

    test("Put Mapper Tags", async () => {
        const event = new CreateMapperJobLog()
        const body = JSON.parse(event.body)
        const { tags, source } = JSON.parse(body?.data?.attributes?.message)
        const bucket = "ph-origin-files"
        const s3 = new S3Handler()
        await s3.putTags(bucket, source, tags)
    })

    test("ETL", async () => {
        const event = new CreateETL()
        // console.info(JSON.stringify(event))
        const app = require("../../app.js")
        await app.lambdaHandler(event, undefined)
    }, 1000 * 60 * 10)
})
