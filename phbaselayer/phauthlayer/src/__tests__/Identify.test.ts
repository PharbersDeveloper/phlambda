import { Errors2response, identify } from "../index"
import * as fs from "fs"
import {ConfigRegistered, Logger, SF, Store, RedisConfig, AWSRequest} from "phnodelayer"
import { ServerResponse } from "http"
let rds: any = null
let scope: string = "APP|phcommon:accounts:qtaGDePl1OrSFEgm:W,phcommon:parthers:psNeInomlGaSfgvd:R|W#APP|entry:assets&filter[parthers]=psNeInomlGaSfgvd:*:R,entry:assets&filter[owner]=qtaGDePl1OrSFEgm:*:W|W#APP|reports:parthers:5xeiSaYk_1noz-RKPyJ8:R,reports:templates:fVxL1xByKMkIAW1ct_su:R|R"
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

const UnauthorizedNOParthersProperty = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync(path, "utf-8"))
    event.path = "/entry/assets"
    event.headers.Authorization = "5092934c502f725ef082c4ad153a4f848a0ca9f734eb8760478ca22a8416192e"
    event.httpMethod = "GET"
    event.queryStringParameters = {
    }
    event.pathParameters = {
        "type": "assets",
        "id": "testid"
    }
    event.multiValueQueryStringParameters = {
    }
    return event
})

const AccessParthersProperty = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync(path, "utf-8"))
    event.path = "/entry/assets"
    event.headers.Authorization = "5092934c502f725ef082c4ad153a4f848a0ca9f734eb8760478ca22a8416192e"
    event.httpMethod = "GET"
    event.queryStringParameters = {
        "filter[parthers]": "psNeInomlGaSfgvd"
    }
    event.pathParameters = {
        "type": "assets",
    }
    event.multiValueQueryStringParameters = {
    }
    return event
})

const AccessOwnerProperty = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync(path, "utf-8"))
    event.path = "/entry/assets"
    event.headers.Authorization = "5092934c502f725ef082c4ad153a4f848a0ca9f734eb8760478ca22a8416192e"
    event.httpMethod = "GET"
    event.queryStringParameters = {
        "filter[owner]": "qtaGDePl1OrSFEgm"
    }
    event.pathParameters = {
        "type": "assets",
    }
    event.multiValueQueryStringParameters = {
    }
    return event
})

const ScopeReadAccessWrite = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync(path, "utf-8"))
    event.path = "/entry/assets"
    event.headers.Authorization = "5092934c502f725ef082c4ad153a4f848a0ca9f734eb8760478ca22a8416192e"
    event.httpMethod = "PATCH"
    event.queryStringParameters = {
        "filter[owner]": "qtaGDePl1OrSFEgm"
    }
    event.pathParameters = {
        "type": "assets",
    }
    event.multiValueQueryStringParameters = {
    }
    event.body = JSON.stringify({name: "test"})
    return event
})

beforeAll(() => {
    const conf = new RedisConfig("token", "", "", "127.0.0.1", 6379, "0")
    ConfigRegistered.getInstance.registered(conf)
    rds = SF.getInstance.get(Store.Redis)
    if (rds) rds.open()
})

test("权限Access", async () => {
    if (rds) {
        const event = new Access()
        const result = await rds.find("access", null, {match: {token: event.headers.Authorization}})
        if (result.payload.records.length === 1 ) {
            scope = result.payload.records[0].scope
            const flag = identify(event, scope)
            expect(flag.status).toBe(200)
            expect(typeof flag.message).toBe("object")
            expect(flag.message.message).toBe("Access")
        }
    }
})

test("权限Unauthorized By No Parthers Property", async ()=> {
    if (rds) {
        const event = new UnauthorizedNOParthersProperty()
        const result = await rds.find("access", null, {match: {token: event.headers.Authorization}})
        if (result.payload.records.length === 1 ) {
            scope = result.payload.records[0].scope
            const flag = identify(event, scope)
            expect(flag.status).toBe(403)
            expect(typeof flag.message).toBe("object")
            expect(flag.message.message).toBe("Access to Unauthorized")
        }
    }
})

test("权限Access By Parthers Property", async () => {
    if (rds) {
        const event = new AccessParthersProperty()
        const result = await rds.find("access", null, {match: {token: event.headers.Authorization}})
        if (result.payload.records.length === 1 ) {
            scope = result.payload.records[0].scope
            const flag = identify(event, scope)
            expect(flag.status).toBe(200)
            expect(typeof flag.message).toBe("object")
            expect(flag.message.message).toBe("Access")
        }
    }
})

test("权限Access By Owner Property", async () => {
    if (rds) {
        const event = new AccessOwnerProperty()
        const result = await rds.find("access", null, {match: {token: event.headers.Authorization}})
        if (result.payload.records.length === 1 ) {
            scope = result.payload.records[0].scope
            const flag = identify(event, scope)
            expect(flag.status).toBe(200)
            expect(typeof flag.message).toBe("object")
            expect(flag.message.message).toBe("Access")
        }
    }
})

test("Scope is null", () => {
    const event = new AccessOwnerProperty()
    scope = null
    const flag = identify(event, scope)
    expect(flag.status).toBe(403)
    expect(typeof flag.message).toBe("object")
    expect(flag.message.message).toBe("Access to Unauthorized")
})

test("Scope is Super Admin", () => {
    const event = new AccessOwnerProperty()
    scope = "*"
    const flag = identify(event, scope)
    expect(flag.status).toBe(200)
    expect(typeof flag.message).toBe("object")
    expect(flag.message.message).toBe("Access")
})

test("scope is admin is Read", () => {
    const event = new AccessOwnerProperty()
    scope = "APP|*|R"
    const flag = identify(event, scope)
    expect(flag.status).toBe(200)
    expect(typeof flag.message).toBe("object")
    expect(flag.message.message).toBe("Access")
})

test("scope is entry resource in all is read", () => {
    const event = new AccessOwnerProperty()
    scope = "APP|entry:*:*:R|R"
    const flag = identify(event, scope)
    expect(flag.status).toBe(200)
    expect(typeof flag.message).toBe("object")
    expect(flag.message.message).toBe("Access")
})

test("scope is read access is Write", () => {
    const event = new ScopeReadAccessWrite()
    scope = "APP|entry:*:*:R|R"
    const flag = identify(event, scope)
    expect(flag.status).toBe(403)
    expect(typeof flag.message).toBe("object")
    expect(flag.message.message).toBe("Access to Unauthorized")
})

test("error response", () => {
    const event = new Access()
    const req = new AWSRequest(event, "phcommon")
    const response = new ServerResponse(req)
    scope = null
    const flag = identify(event, scope)
    Errors2response(flag, response)
    expect(response.statusCode).toBe(403)
    expect(typeof response["body"]).toBe("object")
    expect(response["body"].message).toBe("Access to Unauthorized")
})

afterAll(() => {
    if (rds) rds.close()
})
