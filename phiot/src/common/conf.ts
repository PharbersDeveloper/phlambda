import phS3Facade from "./s3facade/phS3Facade"

export default class Conf {
    public static endpoint = "ajh20s05b2cxs-ats.iot.ap-southeast-1.amazonaws.com"
    public static caFile = "root-CA.crt"
    public static cert = "all-certificate.pem.crt"
    public static key = "private.pem.key"
    public static count = 10
    public static websocket = false
    public static region = "ap-southeast-1"
    public static async getCaFile() {
        const result = await phS3Facade.getObject("ph-", "")
        return String(result)
    }

    public static async getCertFile() {
        const result = await phS3Facade.getObject("ph-", "")
        return String(result)
    }

    public static async getKeyFile() {
        const result = await phS3Facade.getObject("ph-", "")
        return String(result)
    }
}
