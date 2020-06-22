'use strict';

const app = require('../../app.js')
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;
const mongoose = require("mongoose")

describe('Tests index', function () {
    it('verify find one successfully', async () => {
        const event = JSON.parse(fs.readFileSync("../events/event_success_find_one.json", 'utf8'))
        const result = await app.lambdaHandler(event, context)

        expect(result).to.be.an('object');
        expect(result.statusCode).to.equal(200);
        expect(result.body).to.be.an('string');

        let response = JSON.parse(result.body);

        expect(response).to.be.an('object');
        expect(response.data.id).to.be.equal("5e00862a28e9fe103c5e2f4e");
        expect(response.data.type).to.be.equal("proposals");
        // expect(response.location).to.be.an("string");
    });

    after("desconnect db", async () => {
        await mongoose.disconnect()
    });
});
