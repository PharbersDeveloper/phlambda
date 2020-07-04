'use strict';

const delegate = require("../../dist/delegate/appLambdaDelegate").default
const phlogger = require("../../dist/logger/phLogger").default
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;

describe('Tests index', function () {
	it('test import one', async () => {
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
		await app.store.disconnect()
	});
});
