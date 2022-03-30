import { LambdaClient } from "@aws-sdk/client-lambda"
import { AWSRegion } from "../constants/common"

export default class AWSLambda {
    private readonly client: any = null

    constructor() {
        this.client = new LambdaClient({
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
