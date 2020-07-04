'use strict';

// const app = require('../../app.js')
const delegate = require("../../dist/delegate/appLambdaDelegate").default
const phlogger = require("../../dist/logger/phLogger").default
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;
// const mongoose = require("mongoose")

describe('Tests index', function () {
	// it('verify find one successfully', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_success_find_one.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)
	//
	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(200);
	//     expect(result.body).to.be.an('string');
	//
	//     let response = JSON.parse(result.body);
	//
	//     expect(response).to.be.an('object');
	//     expect(response.data.id).to.be.equal("5efda2795320f5c502615d39");
	//     expect(response.data.type).to.be.equal("images");
	//     // expect(response.location).to.be.an("string");
	// });
	//
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
	//     expect(result).to.be.an('object');
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
	//
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

	//  it('verify patch one', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_success_patch_one.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)

	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(200);
	//     expect(result.body).to.be.an('string');

	//     let response = JSON.parse(result.body);

	//     expect(response).to.be.an('object');
	//     expect(response.data.type).to.be.equal("proposals");
	//     expect(response.data.attributes.describe).to.be.equal("修改-辅助地区经理进行区域管理实战模拟测试与练习工具");
	//     // expect(response.location).to.be.an("string");
	// });

	it('verify patch one', async () => {
		const app = new delegate()
		app.prepare().then(() => {
			phlogger.info("connect db success")
		}).catch(e => {
			phlogger.error("connect db error")
			phlogger.error(e)
		})

		const record1 =
			{
				path: "path01",
				tag: "tag"
			}

		const record2 =
			{
				path: "path02",
				tag: "tag"
			}
		const result1 = await app.store.create("image", record1)
		const result2 = await app.store.create("image", record2)
		//
		const record0 =
			{
				title: 'alfred test',
				subTitle: 'alfred test sub',
				startDate: new Date(2011, 5, 30),
				endDate: new Date(),
				location: "武汉wuhan",
				city: "武汉",
				activityType: "a",
				contentTitle: "b",
				contentDesc: "c",
				language: 1,
				logo: result1.payload.records[0].id,
				logoOnTime: result2.payload.records[0].id
			}

		const result3 = await app.store.create("activity", record0)
		phlogger.info(result3)
		// const result = await app.store.find("image", "FGVE7yKtnyvyheTyutah")
		// const result = await app.store.delete("image", "mZBp1BgU5suUrfTlCY56")

		expect(result).to.be.an('object');
		expect(result.statusCode).to.equal(200);
		expect(result.body).to.be.an('string');

		let response = JSON.parse(result.body);

		expect(response).to.be.an('object');
		expect(response.data.type).to.be.equal("proposals");
		expect(response.data.attributes.describe).to.be.equal("修改-辅助地区经理进行区域管理实战模拟测试与练习工具");
		// expect(response.location).to.be.an("string");
	}).timeout(30 * 1000)

	after("desconnect db", async () => {
		// await mongoose.disconnect()
		await app.store.disconnect()
	});
});
