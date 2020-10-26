'use strict';

const app = require('../../app.js')
const delegate = require("../../dist/delegate/appLambdaDelegate").default
const phLogger = require("phnodelayer").logger
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')

describe('Tests index', function () {

	// it('verify post one', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_success_apply_post_one.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)
	//
	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(201);
	//     expect(result.body).to.be.an('string');
	//
	//     let response = JSON.parse(result.body);
	//
	//     expect(response).to.be.an('object');
	//     expect(response.data.type).to.be.equal("applies");
	//
	// });
	async function sleep(ms) {
		return new Promise((resolve) => {
			setTimeout(() => {
				resolve('')
			}, ms)
		})
	}
	it('verify find one successfully', async () => {
	    const event = JSON.parse(fs.readFileSync("../events/event_success_find_one.json", 'utf8'))
		for (const item of [1,2,3,4,5,6,7,8,9,10]) {
			const result = await app.lambdaHandler(event, context)
			phLogger.info(JSON.stringify(JSON.parse(result.body)))
		}
		await sleep(1000 * 60)
	    // expect(result).to.be.an('object');
	    // expect(result.statusCode).to.equal(200);
	    // expect(result.body).to.be.an('string');
		//
	    // let response = JSON.parse(result.body);
	    // phLogger.info(response)
		//
	    // expect(response).to.be.an('object');
	    // expect(response.data.id).to.be.equal("n5DzBBvCCuVANODXHbfm");
	    // expect(response.data.type).to.be.equal("images");
	    // expect(response.location).to.be.an("string");
	});

	// it('verify find one error', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_error_find_one.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)
	//
	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(404);
	//     expect(result.body).to.be.an('string');
	//
	//     let response = JSON.parse(result.body);
	//
	//     expect(response).to.be.an('object');
	//     expect(response.errors[0].detail).to.be.equal("Invalid ID.");
	//     expect(response.errors[0].title).to.be.equal("One or more of the targeted resources could not be found.");
	//     // expect(response.location).to.be.an("string");
	// });
	//
	// it('verify find relationship success', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_success_find_relationships.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)
	//
	// 	expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(200);
	//     expect(result.body).to.be.an('string');
	//
	//     let response = JSON.parse(result.body);
	//
	//     expect(response).to.be.an('object');
	//     expect(response.data[0].type).to.be.equal("products");
	//     expect(response.data[0].id).to.be.equal("5e00862a28e9fe103c5e2f2d");
	//     // expect(response.location).to.be.an("string");
	// });

	// it('verify find page success', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_success_find_page.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)
	//
	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(200);
	//     expect(result.body).to.be.an('string');
	//
	//     let response = JSON.parse(result.body);
	//
	//     expect(response).to.be.an('object');
	//     expect(response.data[0].type).to.be.equal("proposals");
	//     expect(response.data.length).to.be.equal(1);
	//     // expect(response.location).to.be.an("string");
	// });
	//
	// it('verify find filter page', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_success_find_filter.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)
	//
	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(200);
	//     expect(result.body).to.be.an('string');
	//
	//     let response = JSON.parse(result.body);
	//
	//     expect(response).to.be.an('object');
	//     expect(response.data[0].type).to.be.equal("proposals");
	//     expect(response.data.length).to.be.equal(1);
	//     // expect(response.location).to.be.an("string");
	// });

	// it('verify find sort', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_success_find_sort.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)

	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(200);
	//     expect(result.body).to.be.an('string');

	//     let response = JSON.parse(result.body);

	//     expect(response).to.be.an('object');
	//     expect(response.data[0].id).to.be.equal("5e00862c28e9fe103c5e3019");
	//     expect(response.data[1].id).to.be.equal("5e00862a28e9fe103c5e2f4e");
	//     // expect(response.location).to.be.an("string");
	// });


	// it('verify delete one', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_success_delete_one.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)

	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(204);

	//     // let response = JSON.parse(result.body);

	//     // expect(response).to.be.an('object');
	//     // expect(response.data.length).to.be.equal(0);
	// });

	// it('verify post one', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_success_post_one.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)
	//
	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(201);
	//     expect(result.body).to.be.an('string');
	//
	//     let response = JSON.parse(result.body);
	//
	//     expect(response).to.be.an('object');
	//     expect(response.data.type).to.be.equal("proposals");
	//
	// });
	//
	// it('verify find ids success', async () => {
	// 	const event = JSON.parse(fs.readFileSync("../events/event_success_find_ids.json", 'utf8'))
	// 	const result = await app.lambdaHandler(event, context)
	//
	// 	expect(result).to.be.an('object');
	// 	expect(result.statusCode).to.equal(200);
	// 	expect(result.body).to.be.an('string');
	//
	// 	let response = JSON.parse(result.body);
	// 	phLogger.info(response)
	//
	// 	expect(response).to.be.an('object');
	// 	expect(response.data.id).to.be.equal("n5DzBBvCCuVANODXHbfm");
	// 	expect(response.data.type).to.be.equal("images");
	// 	// expect(response.location).to.be.an("string");
	// });
	//
	//  it('verify patch one', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_success_patch_one.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)
	//
	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(200);
	//     expect(result.body).to.be.an('string');
	//
	//     let response = JSON.parse(result.body);
	//
	//     expect(response).to.be.an('object');
	//     expect(response.data.type).to.be.equal("reports");
	//     expect(response.data.attributes.describe).to.be.equal("《修改-广阔市场用药分析及展望》")
	//     // expect(response.location).to.be.an("string");
	// });
});
