import * as fs from "fs"
import { Logger } from "phnodelayer"

const answer = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/answers"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "answers"
    }
    return event
})

const evaluation = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/evaluations"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "evaluations"
    }
    return event
})

const final = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/finals"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "finals"
    }
    return event
})

const hospital = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/hospitals"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "hospitals"
    }
    return event
})

const image = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/images"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "images"
    }
    return event
})

const level = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/levels"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "levels"
    }
    return event
})

const period = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/periods"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "periods"
    }
    return event
})

const policy = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/policies"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "policies"
    }
    return event
})

const preset = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/presets"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "presets"
    }
    return event
})

const product = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/products"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "products"
    }
    return event
})

const project = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/projects"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "projects"
    }
    return event
})

const proposal = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/proposals"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "proposals"
    }
    return event
})

const region = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/regions"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "regions"
    }
    return event
})

const report = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/reports"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "reports"
    }
    return event
})

const requirement = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/requirements"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "requirements"
    }
    return event
})

const resource = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/resources"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "resources"
    }
    return event
})

const usableProposal = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/usable-proposals"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "usable-proposals"
    }
    return event
})

const validation = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_find.json", "utf8"))
    event.path = "/ntm/validations"
    event.httpMethod = "GET"
    event.pathParameters = {
        type: "validations"
    }
    return event
})

const projectExport = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/ntm/event_ntm_post_export.json", "utf8"))
    event.path = "/ntm/projects"
    event.httpMethod = "POST"
    event.pathParameters = {
        type: "export"
    }
    return event
})

test("Find projectExport", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new projectExport(), undefined)
    console.log(result)
}, 1000 * 60)

test("Find validation", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new validation(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find usableProposal", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new usableProposal(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find images", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new image(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find resource", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new resource(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find requirement", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new requirement(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find report", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new report(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find region", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new region(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find proposal", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new proposal(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find project", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new project(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find product", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new product(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find preset", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new preset(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find policy", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new policy(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find period", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new period(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find level", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new level(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find hospital", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new hospital(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find answer", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new answer(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find evaluations", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new evaluation(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)

test("Find finals", async () => {
    const app = require("../../app.js")
    const result = await app.lambdaHandler(new evaluation(), undefined)
    expect(result.statusCode).toBe(200)
}, 1000 * 60)
