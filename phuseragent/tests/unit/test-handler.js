'use strict';

const delegate = require("../../dist/delegate/appLambdaViewAgentDelegate").default
const phLogger = require("../../dist/logger/phLogger").default
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;
const CryptoJS = require("crypto-js");
// const mongoose = require("mongoose")

function hexEncode(value) {
	return value.toString(CryptoJS.enc.Hex);
}

function hmac(secret, value) {
	return CryptoJS.HmacSHA256(value, secret, {asBytes: true});
}

function hash(value) {
	return CryptoJS.SHA256(value);
}

describe('Tests index', function () {
	const del = new delegate()
	before("before all", async () => {
		await del.prepare()
	})
	// it('init common database', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_init_comment_database.json", 'utf8'))
	// 	const clients = event["clients"]
	// 	const crs = await Promise.all(clients.map(async (c) => {
	// 		const tmp = c.id
	// 		delete c.id
	// 		c.seed = "alfred test"
	// 		c.created = new Date()
	// 		const need = String(tmp) + c.seed + c.created.toString()
	// 		c.secret = hexEncode(hmac(c.created.toString().substr(0,8), need))
	// 		const isr = await del.store.create("client", c)
	// 		return { id: tmp, dbid: isr.payload.records[0].id }
	// 	}))
	// 	phlogger.info(crs)
	//
	// 	const components = event["components"]
	// 	const cprs = await Promise.all(components.map(async (c) => {
	// 		const tmp = c.id
	// 		delete c.id
	// 		c.created = new Date();
	// 		c.updated = new Date();
	//
	// 		const ids = c.client
	// 		c.client = ids.map(x => crs.find(y => y.id === x).dbid)
	//
	// 		const isr = await del.store.create("component", c)
	// 		return { id: tmp, dbid: isr.payload.records[0].id }
	// 	}))
	// 	phlogger.info(cprs)
	//
	// 	const partners = event["partners"]
	// 	const prs = await Promise.all(partners.map(async (c) => {
	// 		const tmp = c.id
	// 		delete c.id
	//
	// 		const isr = await del.store.create("partner", c)
	// 		return { id: tmp, dbid: isr.payload.records[0].id }
	// 	}))
	// 	phlogger.info(prs)
	//
	// 	const roles = event["roles"]
	// 	const rrs = await Promise.all(roles.map(async (c) => {
	// 		const tmp = c.id
	// 		delete c.id
	//
	// 		const isr = await del.store.create("role", c)
	// 		return { id: tmp, dbid: isr.payload.records[0].id }
	// 	}))
	// 	phlogger.info(rrs)
	//
	// 	const scopes = event["scopes"]
	// 	const srs = await Promise.all(scopes.map(async (c) => {
	// 		const tmp = c.id
	// 		delete c.id
	//
	// 		const ids = c.owner
	// 		c.owner = ids.map(x => rrs.find(y => y.id === x).dbid)
	//
	// 		const isr = await del.store.create("scope", c)
	// 		return { id: tmp, dbid: isr.payload.records[0].id }
	// 	}))
	// 	phlogger.info(srs)
	//
	// 	const accounts = event["accounts"]
	// 	const accs = await Promise.all(accounts.map(async (c) => {
	// 		const tmp = c.id
	// 		delete c.id
	//
	// 		const rid = c.defaultRole
	// 		c.defaultRole = rrs.find(y => y.id === rid).dbid
	//
	// 		const cid = c.employer
	// 		c.employer = prs.find(y => y.id === cid).dbid
	//
	// 		const pwd = "Abcde196125"
	// 		c.password = hexEncode(hash(pwd))
	//
	// 		const isr = await del.store.create("account", c)
	// 		return { id: tmp, dbid: isr.payload.records[0].id }
	// 	}))
	// 	phlogger.info(accs)
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
	// }).timeout(30* 1000)

	it('verify find components successfully', async () => {
		const event = JSON.parse(fs.readFileSync("../events/event_ember_views_find_one.json", 'utf8'))
		const result = await del.exec(event)

		const resultOutput = result.output[0].split("\r\n")
		const corsHeader =   {
			"Access-Control-Allow-Headers" : "Content-Type",
			"Access-Control-Allow-Origin": "*",
			"Access-Control-Allow-Methods": "POST,GET"
		}
		let objHeader = {}
		for (let index = 0; index < resultOutput.length; index++) {
			const element = resultOutput[index].split(":");
			if (element.length === 2) {
				objHeader[element[0]] = element[1]
			}
		}
		Object.assign(objHeader, corsHeader)

		const response = {
			'statusCode': result.statusCode,
			'headers': objHeader,
			'body': String(result.output[1])
		}

		expect(response).to.be.an('object');
		expect(response.statusCode).to.equal(200);
		expect(response.body).to.be.an('string');

		let data = response.body;

		expect(data).to.be.an('string');
		phLogger.info(response)
		// expect(data).to.be.equal("<h2>Hello {{name}}</h2>\n<p>Hello, p.{{name}}</p>");
		// expect(response.location).to.be.an("string");
	});

	after("desconnect db", async () => {
		// await mongoose.disconnect()
		await app.cleanUp()
	});
});
