import { Logger, DBConfig, JSONAPI, StoreEnum, ServerRegisterConfig } from "../index"
import * as fs from "fs"
import {eventNames} from "cluster"

const findIDSEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("events/event_ids.json", "utf8"))
    event.httpMethod = "GET"
    event.path = "/phplatform/projects"
    event.queryStringParameters = {
        "ids[]": "JfSmQBYUpyb4jsei"
    }
    event.multiValueQueryStringParameters = {
        "ids[]": [
            "JfSmQBYUpyb4jsei"
        ]
    }
    return event
})

const findIDEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("events/event_ids.json", "utf8"))
    event.httpMethod = "GET"
    // event.resource = "/phplatform/{type}/{id}"
    event.resource = "/phplatform/{type}/{id}/{relationship}"
    // event.resource = "/phplatform/{type}/{id}/{relationship}"
    // event.resource = "/phplatform/{type}/{id}/relationships/{relationship}"
    // event.path = "/phplatform/accounts/5UBSLZvV0w9zh7-lZQap"
    event.path = "/phplatform/roles/bF8M0Ti9O3qIwadh/accountRole"
    // event.path = "/phplatform/accounts/5UBSLZvV0w9zh7-lZQap/employer"
    // event.path = "/phplatform/partners/zudIcG_17yj8CEUoCTHg/relationships/employee"
    event.pathParameters = {
        // type: "partners",
        // type: "accounts",
        type: "roles",
        // id: "zudIcG_17yj8CEUoCTHg",
        // id: "5UBSLZvV0w9zh7-lZQap",
        id: "bF8M0Ti9O3qIwadh",
        relationship: "accountRole"
    }
    event.queryStringParameters = {

    }
    event.multiValueQueryStringParameters = {
    }
    return event
})


const createEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("events/event_ids.json", "utf8"))
    event.httpMethod = "POST"
    event.path = "/phplatform/projects"
    event.body = JSON.stringify({
        data: {
            type: "projects",
            attributes: {
                id: "OFuZPd7G_JA1QOYIs3ku",
                name: "Alex Test",
                type: "Alex Test"
            }
        }
    })
    event.queryStringParameters = {
    }
    event.multiValueQueryStringParameters = {
    }
    return event
})

const updateEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("events/event_ids.json", "utf8"))
    event.httpMethod = "PATCH"
    event.resource = "/phplatform/{type}/{id}"
    event.path = "/phplatform/projects/OFuZPd7G_JA1QOYIs3ku"
    event.body = JSON.stringify({
        data: {
            type: "projects",
            id: "OFuZPd7G_JA1QOYIs3ku",
            attributes: {
                name: "Alex Test1",
                type: "Alex Test1",
                provider: "",
                owner: "",
                created: new Date(),
                models: [],
                scripts: [],
                datasets: [],
                flow: "",
                analysis: "",
                notebooks: [],
                dashBoards: [],
                wikis: [],
                tasks: [],
                actions: []
            }
        }
    })
    event.queryStringParameters = {
        id: "OFuZPd7G_JA1QOYIs3ku"
    }
    event.multiValueQueryStringParameters = {
    }
    return event
})

const deleteEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("events/event_ids.json", "utf8"))
    event.httpMethod = "DELETE"
    event.resource = "/phplatform/{type}/{id}"
    event.path = "/phplatform/projects/OFuZPd7G_JA1QOYIs3ku"
    event.queryStringParameters = {
        id: "OFuZPd7G_JA1QOYIs3ku"
    }
    event.multiValueQueryStringParameters = {
    }
    return event
})


const registerConfigs = jest.fn(() => {
    const jsonapiDBConfig = new DBConfig({
        name: StoreEnum.POSTGRES,
        entity: "platform",
        database: "phplatform",
        user: "pharbers",
        password: "Abcde196125",
        host: "127.0.0.1",
        port: 5432,
        poolMax: 2
    })
    return [jsonapiDBConfig]
})

describe("IDS Test", () => {

    test("Create", async () => {
        const configs = new registerConfigs()
        ServerRegisterConfig(configs)
        const result = await JSONAPI(StoreEnum.POSTGRES, new createEvent())
        const data = JSON.parse(String(result.outputData[1].data))
        Logger.info(data)
        expect(result.statusCode).toBe(201)
    })

    test("Update", async () => {
        const configs = new registerConfigs()
        ServerRegisterConfig(configs)
        const result = await JSONAPI(StoreEnum.POSTGRES, new updateEvent())
        expect(result.statusCode).toBe(204)
    })

    test("Delete", async () => {
        const configs = new registerConfigs()
        ServerRegisterConfig(configs)
        const result = await JSONAPI(StoreEnum.POSTGRES, new deleteEvent())
        expect(result.statusCode).toBe(204)
    })

    test("Find IDS", async () => {
        const configs = new registerConfigs()
        ServerRegisterConfig(configs)
        const result = await JSONAPI(StoreEnum.POSTGRES, new findIDSEvent())
        const data = JSON.parse(String(result.outputData[1].data))
        Logger.info(data)
        expect(data.data instanceof Array).toBe(true)
    })

    // test("Find ID", async () => {
    //     for (const item of [1, 2, 3]) {
    //         const configs = new registerConfigs()
    //         ServerRegisterConfig(configs)
    //         const result = await JSONAPI(StoreEnum.POSTGRES, new findIDEvent())
    //         const data = JSON.parse(String(result.outputData[1].data))
    //         Logger.info(data)
    //         expect(data.data instanceof Object).toBe(true)
    //     }
    // })
})
