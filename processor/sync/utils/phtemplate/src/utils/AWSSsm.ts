
import { SSMClient } from "@aws-sdk/client-ssm"
import { AWSRegion } from "../constants/common"

export default class AWSSsm {
    private readonly client: SSMClient = null

    constructor() {
        this.client = new SSMClient({
            region: AWSRegion
        })
    }

    getClient() {
        return this.client
    }

    destroy() {
        this.client.destroy()
    }
}
