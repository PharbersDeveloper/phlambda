'use strict';

const app = require('../../app.js')
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;
const mongoose = require("mongoose")

describe('Tests index', function () {
    it('verify find components successfully', async () => {
        const event = JSON.parse(fs.readFileSync("../events/event_ember_views_find_one.json", 'utf8'))
        const result = await app.lambdaHandler(event, context)

        expect(result).to.be.an('object');
        expect(result.statusCode).to.equal(200);
        expect(result.body).to.be.an('string');

        let response = result.body;

        expect(response).to.be.an('string');
        expect(response).to.be.equal("<h2>Hello {{name}}</h2>\n<p>Hello, p.{{name}}</p>");
        // expect(response.location).to.be.an("string");
    });

    after("desconnect db", async () => {
        await mongoose.disconnect()
    });
});
