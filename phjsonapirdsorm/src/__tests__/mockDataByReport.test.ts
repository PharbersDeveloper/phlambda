import { dbFactory, logger } from "phnodelayer"

test("Mock Data", async () => {
    logger.info("Init")
    const store = dbFactory.getInstance.getStore()
    const id = "5xeiSaYk_1noz-RKPyJ8"
    const partner = {
        id,
        pid: "zudIcG_17yj8CEUoCTHg"
    }

    const template = {
        name: "MAX Report",
        partnerTemplate: id,
        source: "",
        rid: "acb82748-99ef-4ede-9b1b-5f45f1290638",
        gid: "1297dd91-22b4-4e4c-bcf0-77b555c7e0f6",
        tag: "None",
        version: "0.0.2",
        description: "MAX V0.0.2"
    }
    await store.create("partner", partner)

    await store.create("template", template)

    await store.disconnect()
    logger.info("End")
})
