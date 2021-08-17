
import { SSMClient } from "@aws-sdk/client-ssm"

export default class AWSSsm {
    private readonly client: SSMClient = null

    constructor(config: any) {
        this.client = new SSMClient(config)
    }

    getClient() {
        return this.client
    }

    destroy() {
        this.client.destroy()
    }
}
