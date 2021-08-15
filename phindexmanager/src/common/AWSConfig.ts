import AWSSts from "../utils/AWSSts"
import Config from "./Config"

export default class AWSConfig extends Config {

    private static instance: AWSConfig = null

    private constructor() {
        super()
    }

    static get getInstance() {
        if (AWSConfig.instance === null) {
            AWSConfig.instance = new AWSConfig()
        }
        return AWSConfig.instance
    }

    async register(names: string[], region: string = "cn-northwest-1") {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey, region)
        for (const name of names) {
            const result = await sts.assumeRole(name, `arn:aws-cn:iam::444603803904:role/${name}`)
            this.typeAnalyzerMap.set(name, result)
        }
    }

    getConf(key: string): Map<string, any> {
        return this.typeAnalyzerMap.get(key)
    }
}
