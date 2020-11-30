import { Errors2response, identify } from "../index"
import * as fs from "fs"
import {ConfigRegistered, Logger, SF, Store, RedisConfig} from "phnodelayer"
let rds: any = null
const path = "../events/event_lambda_auth.json"

const Access = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync(path, "utf-8"))
    event.path = "/phcommon/accounts"
    event.headers.Authorization = "5092934c502f725ef082c4ad153a4f848a0ca9f734eb8760478ca22a8416192e"
    event.httpMethod = "GET"
    event.queryStringParameters = {
        "ids[]": "qtaGDePl1OrSFEgm"
    }
    event.multiValueQueryStringParameters = {
        "ids[]": [
            "qtaGDePl1OrSFEgm"
        ]
    }
    return event
})

beforeAll(() => {
    const conf = new RedisConfig("token", "", "", "127.0.0.1", 6379, "0")
    ConfigRegistered.getInstance.registered(conf)
    rds = SF.getInstance.get(Store.Redis)
    if (rds) rds.open()
})

test("权限Access", async () => {
    // if (rds) {
    //     const event = new Access()
    //     const result = await rds.find("access", null, {match: {token: event.headers.Authorization}})
    //     if (result.payload.records.length === 1 ) {
    //         const scope = result.payload.records[0].scope
    //         const flag = identify(event, scope)
    //         Logger.info(flag)
    //     }
    // }
    const event = new Access()
    const flag = identify(event, "")
    Logger.info(flag)
})

afterAll(() => {
    if (rds) rds.close()
})
