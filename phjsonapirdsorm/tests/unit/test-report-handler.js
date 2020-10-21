// 'use strict';
//
// const app = require('../../app.js')
// const delegate = require("../../dist/delegate/appLambdaDelegate").default
// const phLogger = require("../../dist/logger/phLogger").default
// const chai = require('chai')
// const expect = chai.expect
// const fs = require('fs')
// var context;
// var del;
// // const mongoose = require("mongoose")
//
// describe('Tests index', function () {
//     del = new delegate()
//     before("before all", async () => {
//         if (del.isFirstInit) {
//             await del.prepare()
//         }
//     })
//
//
//     it('init phreports database for max table', async () => {
//         const event = JSON.parse(fs.readFileSync("../events/event_reports_find.json", 'utf8'))
//         const result = await app.lambdaHandler(event, context)
//         phLogger.info(JSON.stringify(JSON.parse(result.body)))
//     }).timeout(1000 * 30)
//
//     after("desconnect db", async () => {
//         // await mongoose.disconnect()
//         await del.cleanUp()
//     });
// });
