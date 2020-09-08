'use strict';

const delegate = require("../../dist/delegate/appLambdaDelegate").default
const phLogger = require("../../dist/logger/phLogger").default
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;
var del;

describe('Tests index', function () {
    del = new delegate()
    before("before all", async () => {
        if (del.isFirstInit) {
            const se = require("../../dist/common/StoreEnum")
            await del.prepare(se.StoreEnum.Postgres)
        }
    })


    it('test layer select db init', async () => {
        phLogger.info(process.cwd())
    }).timeout(1000 * 30)

    after("desconnect db", async () => {
        // await mongoose.disconnect()
        await del.cleanUp()
    });
});
