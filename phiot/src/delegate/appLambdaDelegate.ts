import { QoS } from "aws-crt/dist/common/mqtt"
import { ClientBootstrap } from "aws-crt/dist/native/io"
import { io, iot, mqtt } from "aws-iot-device-sdk-v2"
import { ConfigRegistered, Logger, RedisConfig, SF, Store } from "phnodelayer"
import { IoTConf, RedisConf } from "../common/conf"
import MQTT from "../common/iot"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        try {
            const cert = await IoTConf.getCertFile()
            const key =  await IoTConf.getKeyFile()
            const ca = await IoTConf.getCaFile()
            const mq: MQTT = new MQTT()
            // @ts-ignore
            const body = JSON.parse(event.body)
            await mq.setClientId(body.uid).setCleanSession(false)
                .setClientBootstrap(new io.ClientBootstrap()).setConfigBuilder(cert, key, ca)
                .setEndPoint(IoTConf.endpoint).build()
            await mq.open()
            const message = JSON.stringify(body)
            Logger.info(message)
            await mq.publish(body.topic, QoS.AtLeastOnce, message)
            await mq.close()
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
        }

        // 原始方法
        // // @ts-ignore
        // const body = JSON.parse(event.body)
        // const cert = await IoTConf.getCertFile()
        // const key =  await IoTConf.getKeyFile()
        // const ca = await IoTConf.getCaFile()
        // const clientBootstrap = new io.ClientBootstrap()
        // const configBuilder = iot.AwsIotMqttConnectionConfigBuilder.new_mtls_builder(cert, key)
        // if (ca != null) {
        //     configBuilder.with_certificate_authority(ca)
        // }
        // configBuilder.with_clean_session(false)
        // configBuilder.with_client_id(body.uid)
        // configBuilder.with_endpoint(IoTConf.endpoint)
        // configBuilder.with_keep_alive_seconds(1000 * 5)
        // configBuilder.with_timeout_ms(1000 * 10)
        // const client = new mqtt.MqttClient(clientBootstrap)
        // const config = configBuilder.build()
        // const connection = client.new_connection(config)
        // await connection.connect()
        // await connection.publish(body.topic, JSON.stringify(body), 1)
        // await connection.disconnect()
        // return {
        //     status: 200,
        //     headers: { "Content-Type": "application/json", "Accept": "application/json" },
        //     message: { message: "Success" },
        // }
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
