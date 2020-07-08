'use strict';

const app = require("../../app")
const phlogger = require("../../dist/logger/phLogger").default
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;

describe('Tests index', function () {
	it('test import data from mongodb', async () => {
		const event = JSON.parse(fs.readFileSync("../events/event_import_data_from_excel.json", 'utf8'))
		const result = await app.lambdaHandler(event, context)
		phlogger.info(result)
	}).timeout(30 * 100000)

	after("desconnect db", async () => {
		// await app.store.disconnect()
		// monogoose.disconnect()
	});
});
