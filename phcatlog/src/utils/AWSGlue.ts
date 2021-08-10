import { GlueClient } from "@aws-sdk/client-glue"

export class AWsGlue {
    private readonly client: any = null

    constructor(config: any) {
        this.client = new GlueClient(config)
    }

    getClient() {
        return this.client
    }

    destroy() {
        this.client.destroy()
    }
}
