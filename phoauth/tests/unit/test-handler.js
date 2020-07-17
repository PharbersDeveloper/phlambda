'use strict';

const app = require('../../app.js')
const delegate = require("../../dist/delegate/appLambdaDelegate").default
const phlogger = require("../../dist/logger/phLogger").default
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;
// const mongoose = require("mongoose")

describe('Tests index', function () {
	// it('verify login successfully', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_useragent_login_success.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)
	//
	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(200);
	//     expect(result.body).to.be.an('string');
	//
	//     let response = JSON.parse(result.body);
	//     phlogger.info(response)
	//
	//     expect(response).to.be.an('object');
	//     expect(response.data.id).to.be.equal("n5DzBBvCCuVANODXHbfm");
	//     expect(response.data.type).to.be.equal("images");
	//     // expect(response.location).to.be.an("string");
	// });
	//
	// it('verify authorization successfully', async () => {
	// 	const event = JSON.parse(fs.readFileSync("../events/event_useragent_authorization.json", 'utf8'))
	// 	const result = await app.lambdaHandler(event, context)
	//
	// 	expect(result).to.be.an('object');
	// 	expect(result.statusCode).to.equal(200);
	// 	expect(result.body).to.be.an('string');
	//
	// 	let response = JSON.parse(result.body);
	// 	phlogger.info(response)
	//
	// 	expect(response).to.be.an('object');
	// 	expect(response.data.id).to.be.equal("n5DzBBvCCuVANODXHbfm");
	// 	expect(response.data.type).to.be.equal("images");
	// 	// expect(response.location).to.be.an("string");
	// });

	it('test redis set', async () => {
		const event = JSON.parse(fs.readFileSync("../events/event_useragent_authorization.json", 'utf8'))
		const result = await app.lambdaHandler(event, context)
		phlogger.info(result)
	})

	// it('test token', async () => {
	// 	const event = JSON.parse(fs.readFileSync("../events/event_useragent_token.json", 'utf8'))
	// 	const result = await app.lambdaHandler(event, context)
	// 	phlogger.info(result)
	// })

	// after("desconnect db", async () => {
	// 	// await mongoose.disconnect()
	// 	await app.cleanUp()
	// });
}).timeout(1000 * 3);
