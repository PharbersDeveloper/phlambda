
import { SFNClient } from "@aws-sdk/client-sfn"
import { AWSConfig } from "../common/AWSConfig"

export default class AWSStepFunction {
    private readonly client: SFNClient = null

    constructor() {
        this.client = new SFNClient({
            region: AWSConfig.REGION
        })
    }

    getClient() {
        return this.client
    }

    destroy() {
        this.client.destroy()
    }

}
