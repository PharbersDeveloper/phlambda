import { Logger, DBConfig, JSONAPI, StoreEnum, ServerRegisterConfig } from "../index"
import * as fs from "fs"

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

    test("Find", async () => {
        const configs = new registerConfigs()
        ServerRegisterConfig(configs)
        const result = await JSONAPI(StoreEnum.POSTGRES, new findIDSEvent())
        const data = JSON.parse(String(result.outputData[1].data))
        Logger.info(data)
        expect(data.data instanceof Array).toBe(true)
    })
})
