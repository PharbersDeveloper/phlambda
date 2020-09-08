'use strict';

const phLogger = require("phlayer").phLogger
const app = require('../../app.js')
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;
var del;

describe('Tests index', function () {

	it('test ph layer', async () => {
		const event = JSON.parse(fs.readFileSync("../events/event_useragent_view_find.json", 'utf8'))
		const result = await app.lambdaHandler(event, context)
		phLogger.info(JSON.stringify(JSON.parse(result.body)))
	})

});
