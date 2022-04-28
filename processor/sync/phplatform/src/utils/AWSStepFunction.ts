
import { SFNClient } from "@aws-sdk/client-sfn"
import { AWSRegion } from "../constants/common"

export default class AWSStepFunction {
    private readonly client: SFNClient = null

    constructor() {
        this.client = new SFNClient({
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
