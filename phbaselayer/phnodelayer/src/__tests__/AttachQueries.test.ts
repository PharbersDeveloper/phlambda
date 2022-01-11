import { Logger, DBConfig, JSONAPI, StoreEnum, ServerRegisterConfig } from "../index"
import * as fs from "fs"


const findEvent = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("events/event_attachQueries.json", "utf8"))
    event.httpMethod = "GET"
    event.path = "/phplatform/projects"
    event.queryStringParameters = {
        "filter%5Bname%5D": "JfSmQBYUpyb4jsei",
        "sort": "name",
        "page[offset]": "aaa",
    }
    event.multiValueQueryStringParameters = {
        "filter[name]": [
            "JfSmQBYUpyb4jsei"
        ]
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

describe("Attach Queries Test", () => {

    test("Query", async () => {
        const configs = new registerConfigs()
        ServerRegisterConfig(configs)
        const result = await JSONAPI(StoreEnum.POSTGRES, new findEvent())
        const data = JSON.parse(String(result.outputData[1].data))
        Logger.info(data)
        expect(data.data instanceof Array).toBe(true)
    })

})

