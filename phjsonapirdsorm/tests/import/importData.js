'use strict';

const app = require('../../app.js')
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;
const mongoose = require("mongoose")

describe('Tests index', function () {

    it('verify import data from excel successfully', async () => {
        const event = JSON.parse(fs.readFileSync("../events/event_import_data_from_excel.json", 'utf8'))
        const result = await app.lambdaHandler(event, context)

    });

    after("desconnect db", async () => {
        await mongoose.disconnect()
    });
});
