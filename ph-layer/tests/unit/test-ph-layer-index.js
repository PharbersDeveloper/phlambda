'use strict';

const index = require("../../index")
const chai = require('chai')
const expect = chai.expect
const fs = require('fs')
var context;
var del;

describe('Tests index', function () {
    before("before all", async () => {
        await index.Main({name: "aa"})
    })


    it('test layer select db init', async () => {
        index.phLogger.info(index.StoreEnum.Redis)
        const redisStore = index.DBFactory.getInstance.getStore(index.StoreEnum.Redis)
        expect(redisStore).to.be.an('object');
    }).timeout(1000 * 30)
});
