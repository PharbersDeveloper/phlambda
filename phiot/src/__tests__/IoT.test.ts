import { QoS } from "aws-crt/dist/common/mqtt"
import { io } from "aws-iot-device-sdk-v2"
import * as fs from "fs"
import { Logger } from "phnodelayer"
import { TextDecoder } from "util"
import { IoTConf, RedisConf } from "../common/conf"
import MQTT from "../common/iot"

const PublishAccess = jest.fn(() => {
    const event = JSON.parse(fs.readFileSync("../events/event_iot_publish.json", "utf-8"))
    return event
})

test("IoT Publish Access", async () => {
    const app = require("../../app.js")
    const res = await app.lambdaHandler(new PublishAccess(), undefined)
    expect(res.statusCode).toEqual(200)
    Logger.info(res)
}, 10000)

test("IoT Subscribe", async () => {

    const sleep = async (duration) => {
        return new Promise((resolve, reject) => {
            setTimeout(resolve, duration)
        })
    }

    const sub = async (topic: string, payload: ArrayBuffer) => {
        const decoder = new TextDecoder("utf8")
        const json = decoder.decode(payload)
        Logger.info(`Publish received on topic ${topic}`)
        Logger.info(json)
    }

    const cert = await IoTConf.getCertFile()
    const key =  await IoTConf.getKeyFile()
    const ca = await IoTConf.getCaFile()
    const mqtt = new MQTT()
    await mqtt.setClientId("002").setCleanSession(false)
        .setClientBootstrap(new io.ClientBootstrap()).setConfigBuilder(cert, key, ca)
        .setEndPoint(IoTConf.endpoint).build()
    await mqtt.open()
    await mqtt.subscribe("pharbers/pid/uid", QoS.AtLeastOnce, sub)
    Logger.info("订阅")

    await sleep(1000 * 60 * 20)
}, 1000 * 60 * 20)
