'use strict';

const phLogger = require("phlayer").phLogger
const DBFactory = require("phlayer").DBFactory
let pg;

describe('convert data', function () {
    before('init', async () => {
        pg = DBFactory.getInstance.getStore()
        phLogger.info(pg)
    })


    it ('c oldAsset to newAsset', async () => {
        const asset = await pg.find("asset")
        phLogger.info(asset)
    })

    it ('c fileIndex to dataBlock', async () => {

    })

    it('c oldDataSet to newDataSet', async () => {

    })

    after("close db", async () => {

    });

});