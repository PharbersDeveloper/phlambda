import * as fs from "fs"
import { Logger } from "phnodelayer"

const CreateProjectFunction = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/max/event_create_project.json", "utf8"))
})

const CreateLogFunction = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/max/event_create_log.json", "utf8"))
})

const UpdateLogFunction = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/max/event_update_log.json", "utf8"))
})

const rangeArray = (start, end) => Array(end - start + 1).fill(0).map((v, i) => i + start)
const currentDate = new Date()
const year = currentDate.getFullYear()
const month = currentDate.getMonth() + 1
const monthArray = rangeArray(month - 5, month)
const projects = ["奥鸿", "倍特", "恩华",
    "汇宇", "泰德", "Amgen",
    "Astellas", "Bayer", "BMS",
    "Lilly", "Pfize", "Servier", "UCB"]

describe("Create Test", () => {
    test("Create Max", async () => {
        const event = new CreateProjectFunction()
        let bodies = []

        for (const m of monthArray) {
            const time = new Date(`${m}/1/${year}`).getTime()
            const inputs = projects.map((provider) => {
                return JSON.stringify({
                    data: {
                        type: "projects",
                        attributes: {
                            provider,
                            actions: JSON.stringify([
                                {
                                    owner: "5UBSLZvV0w9zh7-lZQap",
                                    showName: "钱鹏",
                                    version: "测试文件.xlsx",
                                    code: 0,
                                    jobDesc: "success",
                                    jobCat: "upload",
                                    comments: "测试数据",
                                    message: "",
                                    date: 1629869854734
                                }
                            ]),
                            time
                        }
                    }
                })
            })
            bodies = bodies.concat(inputs)
        }

        for (const item of bodies) {
            event.body = item
            const app = require("../../app.js")
            const result = await app.lambdaHandler(event, undefined)
            expect(result.statusCode).toBe(201)
        }
    })

    test("Create Log", async () => {
        const event = new CreateLogFunction()
        let bodies = []

        for (const m of monthArray) {
            const time = new Date(`${m}/1/${year}`).getTime()
            const inputs = projects.map((provider) => {
                return JSON.stringify({
                    data: {
                        type: "job-logs",
                        attributes: {
                            provider,
                            owner: "5UBSLZvV0w9zh7-lZQap",
                            showName: "钱鹏",
                            version: "测试文件.xlsx",
                            code: 0,
                            jobDesc: "success",
                            jobCat: "upload",
                            comments: "测试数据",
                            message: "",
                            date: 1629869854734,
                            time
                        }
                    }
                })
            })
            bodies = bodies.concat(inputs)
        }

        for (const item of bodies) {
            event.body = item
            const app = require("../../app.js")
            const result = await app.lambdaHandler(event, undefined)
            expect(result.statusCode).toBe(201)
        }
    }, 1000 * 60 * 100)

    test("Update Log", async () => {
        const event = new UpdateLogFunction()
        event.body = JSON.stringify({
            data: {
                type: "job-logs",
                id: "D5wTtNEcR51w52cOPpLq",
                attributes: {
                    jobDesc: "fail"
                }
            }
        })
        const app = require("../../app.js")
        const result = await app.lambdaHandler(event, undefined)
        expect(result.statusCode).toBe(204)
    }, 1000 * 60 * 100)
})
