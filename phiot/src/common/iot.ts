import { ClientBootstrap } from "aws-crt/dist/native/io"
import { iot, mqtt } from "aws-iot-device-sdk-v2"
import { Logger } from "phnodelayer"
import { IoTConf } from "./conf"

export interface IIot {
    build()
    open()
    close()
    setClientBootstrap(cb: any): IIot
    setConfigBuilder(cert: string, key: string, ca: string): IIot
    setClientId(id: string): IIot
    setEndPoint(address: string): IIot
    setCleanSession(b: boolean): IIot
    publish(topic: string, qos: number, message: string)
    subscribe(topic: string, qos: number, fn: any)
}

export default class MQTT implements IIot {
    private connection: mqtt.MqttClientConnection
    private clientBootstrap: ClientBootstrap
    private configBuilder: iot.AwsIotMqttConnectionConfigBuilder
    private client: mqtt.MqttClient
    private clientId: string
    private endPoint: string
    private cleanSession: boolean = false
    private cert: string
    private key: string
    private ca: string

    public setClientBootstrap(cb: any): IIot {
        this.clientBootstrap = cb
        return this
    }

    public setConfigBuilder(cert: string, key: string, ca: string): IIot {
        this.cert = cert
        this.key = key
        this.ca = ca
        return this
    }

    public setClientId(id: string): IIot {
        this.clientId = id
        return this
    }

    public setEndPoint(address: string): IIot {
        this.endPoint = address
        return this
    }

    public setCleanSession(b: boolean): IIot {
        this.cleanSession = b || this.cleanSession
        return this
    }

    public async build() {
        if (IoTConf.websocket) {
            throw new Error("暂不支持WebSocket")
        } else {
            this.configBuilder = iot.AwsIotMqttConnectionConfigBuilder.new_mtls_builder(this.cert, this.key)
        }
        if (this.ca != null) {
            this.configBuilder.with_certificate_authority(this.ca)
        }
        this.configBuilder.with_clean_session(this.cleanSession)
        this.configBuilder.with_client_id(this.clientId)
        this.configBuilder.with_endpoint(this.endPoint)
        this.configBuilder.with_keep_alive_seconds(1000 * 60 * 10)
        this.configBuilder.with_timeout_ms(1000 * 60 * 10)
        // TODO: 并发有问题，先测试@Alex
        if (!this.client) {
            this.client = new mqtt.MqttClient(this.clientBootstrap)
        }
    }

    public async open() {
        const config = this.configBuilder.build()
        this.connection = this.client.new_connection(config)
        this.verify()
        await this.connection.connect()
        Logger.info("Connected")
    }

    public async close() {
        this.verify()
        await this.connection.disconnect()
        Logger.info("Close")
    }

    public async publish(topic: string, qos: number, message: string) {
        this.verify()
        await this.connection.publish(topic, message, qos)
    }

    public async subscribe(topic: string, qos: number, fn: any) {
        return await this.connection.subscribe(topic, qos, fn)
    }

    private verify() {
        if (!this.cert) {throw new Error("cert file is null")}
        if (!this.key) {throw new Error("key file is null")}
        if (!this.ca) {throw new Error("ca file is null")}
        if (!this.clientId) {throw new Error("client_id is null")}
        if (!this.endPoint) {throw new Error("endpoint is null")}
        if (!this.clientBootstrap) {throw new Error("client_bootstrap is null")}
        if (!this.configBuilder) {throw new Error("config_builder is null")}
        if (!this.client) {throw new Error("mqtt client is null")}
        if (!this.connection) {throw new Error("connection is null")}
    }
}
