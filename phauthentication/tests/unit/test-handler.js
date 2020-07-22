'use strict';

const app = require('../../app.js')
const delegate = require("../../dist/delegate/appLambdaDelegate").default
const phLogger = require("../../dist/logger/phLogger").default
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;

describe('Tests index', function () {

    it('verify token auth successfully', async () => {
    	const event = JSON.parse(fs.readFileSync("../events/event_useragent_token_auth.json", 'utf8'))
    	const result = await app.lambdaHandler(event, context)
        phLogger.info(JSON.stringify(result))
    	// expect(result).to.be.an('object');
    	// expect(result.statusCode).to.equal(200);
    	// expect(result.body).to.be.an('string');
		//
    	// let response = JSON.parse(result.body);
    	// phLogger.info(response)
		//
    	// expect(response).to.be.an('object');
    });

	// it('verify login successfully', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_useragent_login_success.json", 'utf8'))
	//     const result = await app.lambdaHandler(event, context)
	//
	//     expect(result).to.be.an('object');
	//     expect(result.statusCode).to.equal(200);
	//     expect(result.body).to.be.an('string');
	//
	//     let response = JSON.parse(result.body);
	//     phLogger.info(response)
	//
	//     expect(response).to.be.an('object');
	//     expect(response.data.id).to.be.equal("n5DzBBvCCuVANODXHbfm");
	//     expect(response.data.type).to.be.equal("images");
	//     // expect(response.location).to.be.an("string");
	// });

	// it('verify authorization successfully', async () => {
	// 	const event = JSON.parse(fs.readFileSync("../events/event_useragent_authorization.json", 'utf8'))
	// 	const result = await app.lambdaHandler(event, context)
	//
	// 	expect(result).to.be.an('object');
	// 	expect(result.statusCode).to.equal(200);
	// 	expect(result.body).to.be.an('string');
	//
	// 	let response = JSON.parse(result.body);
	// 	phLogger.info(response)
	//
	// 	expect(response).to.be.an('string');
	// });


	// it('verify token successfully', async () => {
	// 	const event = JSON.parse(fs.readFileSync("../events/event_useragent_token.json", 'utf8'))
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
	// });

	// it('verify redis set successfully', async () => {
	// 	const authCode = { uid: "uid", cid: "cid", code: "code", scope: "scope", create: new Date(), expired: new Date() }
	// 	const delegate = require('../../dist/delegate/appLmabdaAuthDelegate').default
    //     const del = new delegate()
	// 	await del.prepare()
	// 	const key = "authorization"
	// 	await del.redisStore.create(key, authCode)
	// 	const result = await del.redisStore.find(key)
	// 	expect(result).to.be.an('object')
	// 	expect(result.payload.records[0].uid).to.be.eq("uid")
	// })
	//
	// it('verify redis key expire successfully', async () => {
	// 	function sleep(ms){
	// 		return new Promise((resolve)=>setTimeout(resolve,ms))
	// 	}
	//
	// 	const authCode = { uid: "uid", cid: "cid", code: "code", scope: "scope", create: new Date(), expired: new Date() }
	// 	const delegate = require('../../dist/delegate/appLmabdaAuthDelegate').default
	// 	const del = new delegate()
	// 	await del.prepare()
	// 	const key = "authorization"
	// 	const response = await del.redisStore.create(key, authCode)
	// 	await del.setRedisExpire(`${key}:${response.payload.records[0].id}`, 5)
	// 	setTimeout(() => {
	// 		del.redisStore.find(key).then((response, _) => {
	// 			expect(response).to.be.an('object')
	// 			expect(response.payload.records.length).to.be.eq(0)
	// 		})
	// 	}, 5000)
	// 	await sleep(10000)
	// })

	// it('test token', async () => {
	// 	const event = JSON.parse(fs.readFileSync("../events/event_useragent_token.json", 'utf8'))
	// 	const result = await app.lambdaHandler(event, context)
	// 	phLogger.info(result)
	// })

	// after("desconnect db", async () => {
	// 	// await mongoose.disconnect()
	// 	await app.cleanUp()
	// });
}).timeout(1000 * 30);
