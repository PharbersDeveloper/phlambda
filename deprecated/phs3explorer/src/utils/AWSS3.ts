import { S3Client } from "@aws-sdk/client-s3"
import { AWSRegion } from "../constants/common"

export default class AWsS3 {
    private readonly client: any = null

    constructor() {
        this.client = new S3Client({
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
