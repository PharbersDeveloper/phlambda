
import { SFNClient } from "@aws-sdk/client-sfn"

export default class AWSStepFunction {
    private readonly client: SFNClient = null

    constructor(config: any) {
        this.client = new SFNClient(config)
    }

    getClient() {
        return this.client
    }

    destroy() {
        this.client.destroy()
    }

}
