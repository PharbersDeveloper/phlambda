
import { SSMClient } from "@aws-sdk/client-ssm"
import { AWSConfig } from "../common/AWSConfig"

export default class AWSSsm {
    private readonly client: SSMClient = null

    constructor() {
        this.client = new SSMClient({
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
