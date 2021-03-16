import * as fs from "fs"
import { ConfigRegistered, Logger, MongoConfig, SF, Store } from "phnodelayer"
import { MongoConf } from "../common/config"

const DBConnection = jest.fn(() => {
    return JSON.parse(fs.readFileSync("../events/ntm/event_ntm_upload.json", "utf8"))
})

test("Fix Hospital Relationship Image Filed Data", async () => {
    // const app = require("../../app.js")
    // const result = await app.lambdaHandler(new DBConnection(), undefined)
    // Logger.info(String(result.body))
    Logger.info("Fix Start")
    const mongoConf = new MongoConfig(
        "mongodb",
        MongoConf.entry,
        MongoConf.user,
        MongoConf.password,
        MongoConf.url,
        MongoConf.port,
        MongoConf.db
    )
    ConfigRegistered.getInstance.registered(mongoConf)
    const dbIns = SF.getInstance.get(Store.Mongo)
    await dbIns.open()

    const hospitalResult = await dbIns.find("hospital")
    for (const item of hospitalResult.payload.records) {
        const imageResult = await dbIns.find("image", item.avatar)
        const record = {
            id: imageResult.payload.records[0].id,
            replace: { hospitalAvatar: item.id }
        }
        Logger.info(record)
        const upRes = await dbIns.update("image", record)
        Logger.info(upRes)
    }

    await dbIns.close()

    Logger.info("Fix End")
}, 1000 * 60 * 1000)
