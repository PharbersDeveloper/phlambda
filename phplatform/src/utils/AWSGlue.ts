import { GlueClient } from "@aws-sdk/client-glue"
import { AWSRegion } from "../constants/common"

export default class AWSGlue {
    private readonly client: any = null

    constructor() {
        this.client = new GlueClient({
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
