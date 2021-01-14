import phS3Facade from "./s3facade/phS3Facade"

abstract class Config {}

// tslint:disable-next-line:max-classes-per-file
export class IoTConf extends Config {
    public static endpoint = "a23ve0kwl75dll-ats.iot.cn-northwest-1.amazonaws.com.cn"
    public static count = 10
    public static websocket = false
    public static region = "cn-northwest-1"
    public static async getCaFile() {
        const result = await phS3Facade.getObject("ph-platform", "2020-11-11/certificaties/IoT/root-CA.crt")
        return String(result)
    }

    public static async getCertFile() {
        const result =
       await phS3Facade.getObject("ph-platform", "2020-11-11/certificaties/IoT/iot-certificate.pem.crt")
        return String(result)
    }

    public static async getKeyFile() {
        const result = await phS3Facade.getObject("ph-platform", "2020-11-11/certificaties/IoT/iot-private.pem.key")
        return String(result)
    }
}

// tslint:disable-next-line:max-classes-per-file
export class RedisConf extends Config {
    public static url: string = "pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn"
    public static user: string = ""
    public static password: string = ""
    public static entry: string = "token"
    public static port: number = 6379
    public static db: string = "0"
}
