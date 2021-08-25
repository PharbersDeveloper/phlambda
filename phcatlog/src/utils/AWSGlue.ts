import { GlueClient } from "@aws-sdk/client-glue"
import { AWSConfig } from "../common/AWSConfig"

export default class AWsGlue {
    private readonly client: any = null

    constructor() {
        this.client = new GlueClient({
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
