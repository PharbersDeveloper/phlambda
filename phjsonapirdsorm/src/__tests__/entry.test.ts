import * as fs from "fs"

const HookContext = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_find.json", "utf8"))
    // event.queryStringParameters.
    return event
})

const DrugcategoryContext = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_drugcategory.json", "utf8"))
    // event.queryStringParameters.
    return event
})

const DrugrelationshipContext = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_drugrelationship.json", "utf8"))
    // event.queryStringParameters.
    return event
})

const LexiconContext = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_lexicon.json", "utf8"))
    // event.queryStringParameters.
    return event
})

const ProductContext = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_product.json", "utf8"))
    // event.queryStringParameters.
    return event
})

const MolespecContext = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_molespec.json", "utf8"))
    // event.queryStringParameters.
    return event
})

const ManufacturerContext = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_manufacturer.json", "utf8"))
    // event.queryStringParameters.
    return event
})

const DescriptionPostContext = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_descpost.json", "utf8"))
    // event.queryStringParameters.
    return event
})
const DescriptionPatchContext = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_descpatch.json", "utf8"))
    // event.queryStringParameters.
    return event
})

const DescriptionDelContext = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_entry_descdel.json", "utf8"))
    // event.queryStringParameters.
    return event
})

test("Hook Context", async () => {

    for (const a of [1]) {
        const app = require("../../app.js")
        const res = await app.lambdaHandler(new HookContext(), undefined)
        // tslint:disable-next-line:no-console
        console.info(res.body)
    }

}, 1000 * 60 * 2)

test("drugcategory init", async () => {

    const app = require("../../app.js")
    const res = await app.lambdaHandler(new DrugcategoryContext(), undefined)
    // tslint:disable-next-line:no-console
    console.info(res.body)

}, 1000 * 60 * 2)

test("drugrelationship init", async () => {

    const app = require("../../app.js")
    const res = await app.lambdaHandler(new DrugrelationshipContext(), undefined)
    // tslint:disable-next-line:no-console
    console.info(res.body)

}, 1000 * 60 * 2)

test("lexicon init", async () => {

    const app = require("../../app.js")
    const res = await app.lambdaHandler(new LexiconContext(), undefined)
    // tslint:disable-next-line:no-console
    console.info(res.body)

}, 1000 * 60 * 2)

test("Product init", async () => {

    const app = require("../../app.js")
    const res = await app.lambdaHandler(new ProductContext(), undefined)
    // tslint:disable-next-line:no-console
    console.info(res.body)

}, 1000 * 60 * 2)

test("Molespec init", async () => {

    const app = require("../../app.js")
    const res = await app.lambdaHandler(new MolespecContext(), undefined)
    // tslint:disable-next-line:no-console
    console.info(res.body)

}, 1000 * 60 * 2)

test("manufacturer init", async () => {

    const app = require("../../app.js")
    const res = await app.lambdaHandler(new ManufacturerContext(), undefined)
    // tslint:disable-next-line:no-console
    console.info(res.body)

}, 1000 * 60 * 2)

test("description init", async () => {

    const app = require("../../app.js")
    const res = await app.lambdaHandler(new DescriptionPostContext(), undefined)
    // tslint:disable-next-line:no-console
    console.info(res.body)

}, 1000 * 60 * 2)
