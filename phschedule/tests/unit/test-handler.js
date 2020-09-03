'use strict';

const app = require('../../app.js')
const delegate = require("../../dist/delegate/appLambdaDelegate").default
const phLogger = require("../../dist/logger/phLogger").default
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')

describe('Tests index', function () {

	// it('verify push job successfully', async () => {
	//     const event = JSON.parse(fs.readFileSync("../events/event_sqs_push_job_schedule.json", 'utf8'))
	//     await app.lambdaHandler(event, context)
	// });

	// it('verify push ds successfully', async  () => {
	// 	const event = JSON.parse(fs.readFileSync("../events/event_sqs_push_ds_schedule.json", 'utf8'))
	// 	await app.lambdaHandler(event, context)
	// })

	// it ('verify set asset mart tags successfully', async () => {
	// 	const event = JSON.parse(fs.readFileSync("../events/event_sqs_set_assets_mart_tags_schedule.json", 'utf8'))
	// 	await app.lambdaHandler(event, context)
	// })

    // it ('verify asset data mart successfully', async () => {
    //     const event = JSON.parse(fs.readFileSync("../events/event_sqs_assets_data_mart_schedule.json", 'utf8'))
    //     await app.lambdaHandler(event, context)
    // })

    // it ('verify sandbox data set successfully', async () => {
    //     const event = JSON.parse(fs.readFileSync("../events/event_sqs_sandbox_data_set_schedule.json", 'utf8'))
    //     await app.lambdaHandler(event, context)
    // })

    it ("verify convert excel update version", async () => {
        const event = JSON.parse(fs.readFileSync("../events/event_sqs_convert_update_version_schedule.json", 'utf8'))
        await app.lambdaHandler(event, context)
    })



});
