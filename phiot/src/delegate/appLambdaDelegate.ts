import { QoS } from "aws-crt/dist/common/mqtt"
import { io } from "aws-iot-device-sdk-v2"
import { identify } from "phauthlayer"
import { ConfigRegistered, Logger, RedisConfig, SF, Store } from "phnodelayer"
import { IoTConf, RedisConf } from "../common/conf"
import MQTT from "../common/iot"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        let mq: MQTT = null
        try {
            // const flag = await this.verify(event)
            // if (flag.status !== 200) {
            //     return flag
            // }
            const cert = await IoTConf.getCertFile()
            const key =  await IoTConf.getKeyFile()
            const ca = await IoTConf.getCaFile()
            mq = new MQTT()
            // @ts-ignore
            const body = JSON.parse(event.body)
            await mq.setClientId(body.uid).setCleanSession(false)
                .setClientBootstrap(new io.ClientBootstrap()).setConfigBuilder(cert, key, ca)
                .setEndPoint(IoTConf.endpoint).build()
            await mq.open()
            const message = JSON.stringify(body)
            Logger.info(message)
            await mq.publish(body.topic, QoS.AtLeastOnce, message)
            return {
                status: 200,
                headers: { "Content-Type": "application/json", "Accept": "application/json" },
                message: { message: "Success" },
            }
        } catch (e) {
            Logger.error(e)
            return {
                status: 500,
                headers: { "Content-Type": "application/json", "Accept": "application/json" },
                message: { message: e.message },
            }
        } finally {
            if (mq) {
                await mq.close()
            }
        }
    }

    // private async verify(event: Map<string, any>) {
    //     const redis = new RedisConfig(
    //         RedisConf.entry, RedisConf.user,
    //         RedisConf.password, RedisConf.url,
    //         RedisConf.port, RedisConf.db)
    //     ConfigRegistered.getInstance.registered(redis)
    //     const rds = SF.getInstance.get(Store.Redis)
    //     await rds.open()
    //     // @ts-ignore
    //     const result = await rds.find("access", null, {match: {token: event.headers.Authorization}})
    //     await rds.close()
    //     let scope = ""
    //     if (result.payload.records.length > 0) {
    //         scope  = result.payload.records[0].scope
    //     }
    //     return identify(event, scope)
    // }

}
